from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI
import os
import json

from langchain.memory import ConversationBufferMemory
from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)
from dotenv import load_dotenv
load_dotenv()

SUMMARY_TEMPLATE = """Generate song summary based on song data to provide song writter with short info about song. Respond ONLY with summary please."""

IDEAS_GENERATE_TEMPLATE = """As a seasoned scriptwriter for music videos, devise {ideas_number} creative concepts for a video project. Respond ONLY with python list of strings. each string is idea."""

CHOOSE_IDEA_TEMPLATE = """
You are professional video clip script writer.
Choose one of the ideas for video clip choose one that suites best . Respond ONLY with chosen idea. 
"""

SONG_DATA_TEMPLATE = """Here is song data:
Name: {name}
mood: {mood}
Artist: {artist}
Genre: {genre}
lyrics: {lyrics}
"""

FULL_SONG_DATA_TEMPLATE = """Here is song data:
Name: {name}
mood: {mood}
Artist: {artist}
Genre: {genre}
lyrics: {lyrics}
Summary: {summary}
"""

IDEAS_TEMPLATE = """Video Clip Ideas: {ideas}"""

IDEA_TEMPLATE = """Video Clip Idea: {idea}"""
SONG_SUMMARY_TEMPLATE = """Song summary: summary"""
CONCEPT_TEMPLATE = """Video Clip Concept: {concept}"""
SCENARIO_TEMPLATE = """Video Clip Scenario: {scenario}"""
CONCEPT_GENERATE_TEMPLATE = """As a seasoned scriptwriter for music videos. Based on song data and video clip idea generate 30 second video clip concept."""
SCENARIO_GENERATE_TEMPLATE = """As a seasoned scriptwriter for music videos. Based on song data and video clip idea+concept generate 30 second video clip scenario second by second."""


STORY_BOARD_GENERATE_TEMPLATE = """Write video clip storyboard by its info, describe each second.
- On each step ALWAYS describe ALL objects and persons
- Respond with JSON ONLY no yapping where keys are seconds and values - second description. 
- Describe clip from {start} second to {end} second"""

from dataclasses import dataclass

@dataclass
class Song:    
    name:str
    mood:str 
    artist:str
    genre:str
    lyrics:str
    summary:str=None

    def info_for_summarization(self):
        return {
            "name":self.name,
            "mood":self.mood,
            "artist":self.artist,
            "genre":self.genre,
            "lyrics":self.lyrics
        }
    
    def to_dict(self):
        return {
            "summary":self.summary,
            **self.info_for_summarization()
        }


@dataclass
class VideoClip:
    idea:str=None
    visual_aesthetic:str=None
    concept:str=None
    scenario:str=None
    story_board:str=None    


@dataclass 
class ScenarioWriter:
    name: str
    memory: ConversationBufferMemory
    chat: ChatOpenAI
    video_clip:VideoClip
    ideas:list=None

    def summarize_song(self, song:Song):
        self.song=song
        res = self.chat.invoke([
            SystemMessage(
                content=SUMMARY_TEMPLATE
            ),
            HumanMessage(
                content=SONG_DATA_TEMPLATE.format(**song.info_for_summarization())
            ),
        ])
        song.summary = res.content
        return res.content

    def idea_generation(self, ideas_number:int):
        res = self.chat.invoke([
            SystemMessage(
                content=IDEAS_GENERATE_TEMPLATE
            ),
            HumanMessage(
                content=SONG_DATA_TEMPLATE.format(**self.song.info_for_summarization())
            ),
            HumanMessage(
                content=SONG_SUMMARY_TEMPLATE.format(**{"summary":self.song.summary})
            ),
        ])
        # print(res.content)
        self.ideas=res.content
        return res.content

    
    def choose_best_idea(self, ideas):
        res = self.chat.invoke([
            SystemMessage(
                content=CHOOSE_IDEA_TEMPLATE
            ),
            HumanMessage(
                content=IDEAS_TEMPLATE.format(**{"ideas":ideas})
            ),
            HumanMessage(
                content=SONG_DATA_TEMPLATE.format(**self.song.to_dict())
            ),
        ])
        self.video_clip.idea = res.content
        return res.content
    
    def concept_development(self):
        res = self.chat.invoke([
            SystemMessage(
                content=CONCEPT_GENERATE_TEMPLATE
            ),
            HumanMessage(
                content=SONG_DATA_TEMPLATE.format(**self.song.to_dict())
            ),
            HumanMessage(
                content=IDEA_TEMPLATE.format(**{"idea":self.video_clip.idea})
            ),
            HumanMessage(
                content=CONCEPT_TEMPLATE.format(**{"concept":self.video_clip.concept})
            ),
        ])
        self.video_clip.concept = res.content
        return res.content

    # def visual_aesthetic():
    #     pass

    def write_scenario(self):
        res = self.chat.invoke([
            SystemMessage(
                content=SCENARIO_GENERATE_TEMPLATE
            ),
            HumanMessage(
                content=CONCEPT_TEMPLATE.format(**{"concept":self.video_clip.concept})
            ),
            HumanMessage(
                content=IDEA_TEMPLATE.format(**{"idea":self.video_clip.idea})
            ),
            HumanMessage(
                content=SONG_DATA_TEMPLATE.format(**self.song.to_dict())
            ),
        ])
        self.video_clip.scenario = res.content
        return res.content

    def create_story_board(self, start:int, end:int):
        messages = [
            SystemMessage(
                content=STORY_BOARD_GENERATE_TEMPLATE.format(**{'start':start, "end":end})
            ),
            HumanMessage(
                content=SCENARIO_GENERATE_TEMPLATE.format(**{"scenario":self.video_clip.scenario})
            ),
            HumanMessage(
                content=CONCEPT_TEMPLATE.format(**{"concept":self.video_clip.concept})
            ),
            HumanMessage(
                content=IDEA_TEMPLATE.format(**{"idea":self.video_clip.idea})
            ),
        ]
        res = self.chat.invoke(messages)

        self.video_clip.story_board = clean_text(res.content)

        return self.video_clip.story_board

def clean_text(input_text):
    # Define the substrings to be removed
    start_substring = "```json\n"
    end_substring = "```"
    
    # Remove the start substring
    if input_text.startswith(start_substring):
        input_text = input_text[len(start_substring):]
    
    # Remove the end substring
    if input_text.endswith(end_substring):
        input_text = input_text[:-len(end_substring)]
    
    return json.loads(input_text)

name = "Space in Between"
mood = "Sad"
artist = "Jan Blomquist"
genre = "Techno"
lyrics = """
Can't figure out how we got here
Living on decay
The seven words left on paper
Will disconnect the day
And you want, and you want
And you want anything that's clear
And it's all around us as ghosted machines
Would the real be just silent
If there's a hole in the key?
At the bar in the basement
For an hour-glass of tea
Our love is violent
Constant space in between
And the taste has got a texture
Smoke has not a sound
The fabric that was fixed here
Inherent in the ground
And it's all around us as ghosted machines
Would the real be just silent
If there's a hole in the key?
At the bar in the basement
For an hour-glass of tea
Our love is violent
Space in between
And as much as I'd like to
Believe there's a truth
About our illusion, well I've come to conclude
There's just nothing beyond it
The mind can perceive
Except for the pictures in
The space in between
The space in between"""
openapi_api_key=os.getenv('OPENAPI_API_KEY')

def generate_story_board(
    name,
    mood,
    artist,
    genre,
    lyrics, 
    openapi_api_key=openapi_api_key
):
    song = Song(
        name=name,
        mood=mood,
        artist=artist,
        genre=genre,
        lyrics=lyrics,
    )
    video_clip=VideoClip()
    scenario_writer = ScenarioWriter(
        name="Oleg", 
        memory = ConversationBufferMemory(), 
        chat = ChatOpenAI(
            model_name='gpt-4-0125-preview', 
            openai_api_key=openapi_api_key, 
            temperature=0.7
        ),
        video_clip=video_clip,
    )

    summary = scenario_writer.summarize_song(song)

    ideas = scenario_writer.idea_generation(5)

    best_idea = scenario_writer.choose_best_idea(ideas)

    concept = scenario_writer.concept_development()

    scenario = scenario_writer.write_scenario()

    story_board = scenario_writer.create_story_board(0,31)

    res = {str(int(k)*16):v for k,v in story_board.items()}
    with open('res.json', 'w') as file:
        json.dump(res, file, indent=4)

    return res


# generate_story_board(
#     name=name,
#     mood=mood,
#     artist=artist,
#     genre=genre,
#     lyrics=lyrics,
# )

# generate_story_board(
#     name="""Paint It, Black""",
#     mood="""depression, drive, sad""",
#     artist="""Rolling Stones""",
#     genre="""classical rock""",
#     lyrics="""I see a red door
# And I want it painted black
# No colors anymore
# I want them to turn black
# I see the girls walk by
# Dressed in their summer clothes
# I have to turn my head
# Until my darkness goes
# I see a line of cars
# And they're all painted black
# With flowers and my love
# Both never to come back
# I've seen people turn their heads
# And quickly look away
# Like a newborn baby
# It just happens everyday
# I look inside myself
# And see my heart is black
# I see my red door
# I must have it painted black
# Maybe then, I'll fade away
# And not have to face the facts
# It's not easy facing up
# When your whole world is black
# No more will my green sea
# Go turn a deeper blue
# I could not foresee this thing
# Happening to you
# If I look hard enough
# Into the setting sun
# My love will laugh with me
# Before the morning comes
# I see a red door
# And I want it painted black
# No colors anymore
# I want them to turn black
# I see the girls walk by
# Dressed in their summer clothes
# I have to turn my head
# Until my darkness goes
# I wanna see it painted
# Painted black
# Black as night
# Black as coal
# I wanna see the sun
# Blotted out from the sky
# I wanna see it painted, painted, painted
# Painted black, yeah
# """,
# )


generate_story_board(
    name="""Funeral Derangements""",
    mood="""aggressive""",
    artist="""Ice Nine Kills""",
    genre="""Heavy metal""",
    lyrics="""Slave to the plot
Let 'em rot
Or bring 'em back forever
Sometimes
Sometimes, dead is better!
Yeah!
Sometimes
Sometimes, dead is better!

They say "Behind those gates, eternal life awaits"
But those beyond the grave, come back beyond depraved
With Church bells ringing, I'll start digging
Fast, they'll never know he's missing
Now the cat's back in his cage
"Oh my God, Gage!"

We pray to thee our God (it's all my fault)
For the blessings you've provided
Louis, don't do it (from ashes to ashes, from dust to dust)
I have to

I'll see you on the other side
But I'd kill to bring you back tonight
Don't give up, don't let go
I'll make this right (ah, ah, ah, ah, ah)

I'll dig through sorrow and disgust
Ashes to ashes, dust to dust
Don't give up, don't let go
I'll make this right (ah, ah, ah, ah, ah)

Remember
Sometimes
Sometimes, dead is better!
Yeah
Sometimes
Sometimes, dead is better!

They say that time heals all
But I won't heed the call
Buried in misery
Spare me the eulogy
Still, I can't escape this struggle
Driven when push comes to shovel
Whether God's hand or my own
Nothing here is set in stone

Create!
Cremate!
All hail the Cemetary!

I'll see you on the other side
But I'd kill to bring you back tonight
Don't give up, don't let go
I'll make this right (ah, ah, ah, ah, ah)
I'll dig through sorrow and disgust
Ashes to ashes, dust to dust
Don't give up, don't let go
I'll make this right (ah, ah, ah, ah, ah)

Remember
Sometimes
"Dead is better!"

Ah, ha, ha, ha, ha, ha, ha
I played with mommy, now I want to play with you

It all began with a skid on the pavement
It ends here with Funeral Derangements
The flesh is living but the souls have spoiled
The wrath of God lays beneath this soil
The flesh is living but the souls have spoiled
The wrath of God lays beneath this soil

I'll see you on the other side
But I'd kill to bring you back tonight
Don't give up, don't let go
I'll make this right (ah, ah, ah, ah, ah)

I'll dig through sorrow and disgust
Ashes to ashes, dust to dust
Don't give up, don't let go
I'll make this right (ah, ah, ah, ah, ah)

Remember
Sometimes
Sometimes, dead is better!
Ayup!
""")