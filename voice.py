import asyncio
import os
from functools import partial

from anthropic import Anthropic
from dotenv import load_dotenv
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import BotStartedSpeakingFrame, BotStoppedSpeakingFrame, InterruptionFrame, TextFrame, TranscriptionFrame, VADUserStartedSpeakingFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import WorkerRunner
from pipecat.pipeline.task import PipelineWorker
from pipecat.processors.audio.vad_processor import VADProcessor
from pipecat.processors.frame_processor import FrameProcessor, FrameDirection
from pipecat.services.deepgram.stt import DeepgramSTTService
from pipecat.services.deepgram.tts import DeepgramTTSService
from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams

from app.agent.agent import run_agent
from app.models.cart import Cart
from app.repositories.menu import get_menu


class RestaurantAgent(FrameProcessor):
    def __init__(self, client: Anthropic, menu: list):
        super().__init__()
        self._client = client
        self._menu = menu
        self._cart = Cart()
        self._messages = []
        self._bot_is_speaking = False
        self._processing = False
        self._interrupted = False

    async def process_frame(self, frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, VADUserStartedSpeakingFrame):
            if self._bot_is_speaking:
                # Bot was actively playing audio — interrupt it and discard the in-flight response
                self._interrupted = True
                await self.push_frame(InterruptionFrame(), FrameDirection.DOWNSTREAM)
                await self.push_frame(InterruptionFrame(), FrameDirection.UPSTREAM)
            self._bot_is_speaking = False  # allow next transcription through
            await self.push_frame(frame, direction)
        elif isinstance(frame, BotStartedSpeakingFrame):
            self._bot_is_speaking = True
            await self.push_frame(frame, direction)
        elif isinstance(frame, BotStoppedSpeakingFrame):
            self._bot_is_speaking = False
            await self.push_frame(frame, direction)
        elif isinstance(frame, TranscriptionFrame):
            if not self._processing and not self._bot_is_speaking:
                self._processing = True
                self._interrupted = False
                print(f"[STT] {frame.text}")
                try:
                    response, self._cart, self._messages = await asyncio.get_event_loop().run_in_executor(
                        None,
                        partial(run_agent, frame.text, self._client, self._menu, self._cart, self._messages),
                    )
                    if not self._interrupted:
                        await self.push_frame(TextFrame(response))
                finally:
                    self._processing = False
        else:
            await self.push_frame(frame, direction)


async def main():
    load_dotenv()
    anthropic_key = os.environ["ANTHROPIC_API_KEY"]
    deepgram_key = os.environ["DEEPGRAM_API_KEY"]

    client = Anthropic(api_key=anthropic_key)
    menu = get_menu()

    transport = LocalAudioTransport(
        LocalAudioTransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
        )
    )

    vad = VADProcessor(
        vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=1.0)),
    )
    stt = DeepgramSTTService(api_key=deepgram_key)
    tts = DeepgramTTSService(
        api_key=deepgram_key,
        settings=DeepgramTTSService.Settings(voice="aura-asteria-en"),
    )
    agent = RestaurantAgent(client, menu)

    pipeline = Pipeline([
        transport.input(),
        vad,
        stt,
        agent,
        tts,
        transport.output(),
    ])

    print("Welcome to Pragnya Bites! Start speaking...\n")

    runner = WorkerRunner()
    task = PipelineWorker(pipeline)
    await runner.add_workers(task)
    await runner.run()


if __name__ == "__main__":
    asyncio.run(main())
