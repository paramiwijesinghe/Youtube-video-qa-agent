"""Service that loads transcripts from YouTube into LangChain Document objects.

This is the only place where we directly call the YoutubeLoader; everything
else receives already-loaded Document instances.
"""

from langchain_community.document_loaders import YoutubeLoader


class YoutubeTranscriptLoader:
    """Thin wrapper around LangChain's YoutubeLoader."""

    def load(self, url: str):
        """
        Fetch the transcript for a single YouTube URL.

        Returns a list of LangChain Document objects containing the transcript.
        """
        loader = YoutubeLoader.from_youtube_url(
            url,
            add_video_info=False,
            language=["en", "en-US"],
        )
        return loader.load()
