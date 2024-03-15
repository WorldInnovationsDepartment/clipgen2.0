from langchain.prompts.prompt import PromptTemplate


SUMMARY_TEMPLATE = """Generate song summary based on song data to provide song writter with short info about song. Respond ONLY with summary please."""

IDEAS_GENERATE_TEMPLATE = """As a seasoned scriptwriter for music videos, devise {ideas_number} creative concepts for a video project. Respond ONLY with python list of strings. each string is idea."""

CHOOSE_IDEA_TEMPLATE = """
You are professional video clip script writer.
Choose one of the ideas for video clip choose one that suites best . Respond ONLY with chosen idea. 
"""

SONG_DATA_TEMPLATE = """Here is song data:
Name: {name}
Moode: {moode}
Artist: {artist}
Genre: {genre}
Lyricks: {lyricks}
"""

FULL_SONG_DATA_TEMPLATE = """Here is song data:
Name: {name}
Moode: {moode}
Artist: {artist}
Genre: {genre}
Lyricks: {lyricks}
Summary: {summary}
"""

IDEAS_TEMPLATE = """Video Clip Ideas: {ideas}"""

IDEA_TEMPLATE = """Video Clip Idea: {idea}"""
CONCEPT_TEMPLATE = """Video Clip Concept: {concept}"""
CONCEPT_GENERATE_TEMPLATE = """As a seasoned scriptwriter for music videos. Based on song data and video clip idea generate 30 second video clip concept."""
SCENARIO_GENERATE_TEMPLATE = """As a seasoned scriptwriter for music videos. Based on song data and video clip idea+concept generate 30 second video clip scenario second by second."""
