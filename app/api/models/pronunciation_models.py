from pydantic import BaseModel, Field

class PronunciationScoreResponse(BaseModel):
    """
    Defines the structure for the pronunciation score response.
    """
    reference_text: str = Field(..., description="The original, correct text.")
    transcribed_text: str = Field(..., description="The text transcribed from the user's audio.")
    intelligibility_score: float = Field(..., ge=0, le=100, description="Score based on word accuracy (0-100).")
    acoustic_similarity_score: float = Field(..., ge=0, le=100, description="Score based on acoustic feature similarity to the AI voice (0-100).")
    overall_score: float = Field(..., ge=0, le=100, description="A weighted average of the other scores (0-100).")