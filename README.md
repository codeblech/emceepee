# emceepee

idk how many "mcp servers" i got left in me

## what even is this

two broke mcp servers that process youtube videos and generate music memes because apparently that's what passes for productivity these days

- youtube transcription with gemini (we're on the free tier don't judge) [https://puch.ai/mcp/HUbLKIfDQQ]

- music meme generator that turns your spotify/youtube/YTMusic songs into visual depression [https://puch.ai/mcp/ZIL5Cu4BOW]

- honourable mention: a patrick bateman walking to music generator. videos generated but mcp failed because i couuldn't send videos through mcp tools.

## setup or whatever

```bash
# clone this mess
git clone whatever-this-repo-is

# install dependencies (good luck)

uv venv

uv sync

source ./venv/bin/activate
# setup your .env file with api keys you probably don't have
# check the python files for what keys you need
# spoiler alert: it's a lot

# run the servers (if they even work)
python mcp-bearer-token/youtube_gemini.py
python music-memes/music_memes_mcp.py
```

## features that may or may not work (just kidding it all works)

- transcribe youtube videos (under 30 minutes because we're poor)
- turn music urls into memes that reflect your inner sadness
- automatic platform detection (it tries its best)
- parallel processing for videos (sometimes crashes, it's fine)

## why does this exist

honestly i'm not sure anymore. started as a useful tool, ended up as a monument to my declining mental state

the code is held together by hope and claude code answers. use at your own risk.

---

*if this somehow helps you, great. if it doesn't work, that's also great because at least we're all suffering together*