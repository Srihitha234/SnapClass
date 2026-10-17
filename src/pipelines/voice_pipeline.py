from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np
import io
import librosa
import streamlit as st


# =========================================================
# LOAD VOICE ENCODER
# =========================================================

@st.cache_resource
def load_voice_encoder():

    return VoiceEncoder()


# =========================================================
# GET VOICE EMBEDDING
# =========================================================

def get_voice_embedding(audio_bytes):

    try:

        encoder = load_voice_encoder()

        # Load audio and convert to 16 kHz
        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )

        # Preprocess audio
        wav = preprocess_wav(audio)

        # Generate speaker embedding
        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:

        st.error(f"Voice recognition error: {e}")

        return None


# =========================================================
# IDENTIFY SPEAKER
# =========================================================

def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=0.65
):

    # No new embedding or no candidates
    if new_embedding is None or not candidates_dict:

        return None, 0.0

    # Convert new embedding to NumPy
    new_embedding = np.array(new_embedding)

    best_sid = None
    best_score = -1.0

    # Compare against every registered student
    for sid, stored_embedding in candidates_dict.items():

        if stored_embedding is None:
            continue

        # Convert stored embedding to NumPy
        stored_embedding = np.array(
            stored_embedding
        )

        # Cosine similarity
        similarity = np.dot(
            new_embedding,
            stored_embedding
        )

        if similarity > best_score:

            best_score = similarity
            best_sid = sid

    # Check threshold
    if best_score >= threshold:

        return best_sid, best_score

    return None, best_score


# =========================================================
# PROCESS BULK AUDIO
# =========================================================


def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=0.65,
):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.asarray(
        new_embedding, dtype=np.float32
    ).flatten()

    new_norm = np.linalg.norm(new_embedding)

    if new_norm == 0:
        return None, 0.0

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding is None:
            continue

        try:
            stored = np.asarray(
                stored_embedding, dtype=np.float32
            ).flatten()

            if stored.shape != new_embedding.shape:
                continue

            stored_norm = np.linalg.norm(stored)

            if stored_norm == 0:
                continue

            # True cosine similarity
            similarity = float(
                np.dot(new_embedding, stored)
                / (new_norm * stored_norm)
            )

            if similarity > best_score:
                best_score = similarity
                best_sid = sid

        except (TypeError, ValueError):
            continue

    if best_sid is not None and best_score >= threshold:
        return best_sid, best_score

    return None, max(best_score, 0.0)


def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65,
):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True,
        )

        if len(audio) == 0:
            st.warning("The recording contains no audio.")
            return {}

        segments = librosa.effects.split(
            audio,
            top_db=30,
        )

        identified_results = {}
        best_scores = {}

        for start, end in segments:
            if (end - start) < int(sr * 1.0):
                continue

            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)

            if len(wav) == 0:
                continue

            embedding = encoder.embed_utterance(wav)

            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold,
            )

            # Track the best score even if it didn't pass
            # the threshold, for debugging.
            if score > best_scores.get("best", -1.0):
                best_scores["best"] = score

            if sid is not None:
                if score > identified_results.get(sid, -1.0):
                    identified_results[sid] = score

        if not identified_results:
            st.warning(
                "No registered voice matched the recording. "
                f"Best cosine similarity: "
                f"{best_scores.get('best', 0.0):.3f}. "
                "Check the registered voice profiles and recording quality."
            )

        return identified_results

    except Exception as e:
        st.error(f"Bulk audio processing failed: {e}")
        return {}
