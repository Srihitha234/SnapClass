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

def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65
):

    try:

        encoder = load_voice_encoder()

        # Load audio
        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000
        )

        # Find non-silent sections
        segments = librosa.effects.split(
            audio,
            top_db=30
        )

        identified_results = {}

        # Process every audio segment
        for start, end in segments:

            # Ignore segments shorter than 0.5 seconds
            if (end - start) < int(sr * 0.5):

                continue

            # Extract segment
            segment_audio = audio[start:end]

            # Preprocess segment
            wav = preprocess_wav(
                segment_audio
            )

            # Generate embedding
            embedding = encoder.embed_utterance(
                wav
            )

            # Identify speaker
            sid, score = identify_speaker(
                embedding,
                candidates_dict,
                threshold
            )

            # If a speaker was identified
            if sid is not None:

                # First time seeing this student
                if sid not in identified_results:

                    identified_results[sid] = score

                # Keep strongest similarity score
                elif score > identified_results[sid]:

                    identified_results[sid] = score

        # IMPORTANT:
        # Return only AFTER processing all segments
        return identified_results

    except Exception as e:

        st.error(
            f"Bulk process error: {e}"
        )

        return {}