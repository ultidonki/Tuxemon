# SPDX-License-Identifier: GPL-3.0
# Copyright (c) 2014-2024 William Edwards <shadowapex@gmail.com>, Benjamin Bean <superman2k5@gmail.com>
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, final

from tuxemon import audio, prepare
from tuxemon.event.eventaction import EventAction


@final
@dataclass
class PlaySoundAction(EventAction):
    """
    Play a sound from "resources/sounds/".

    Script usage:
        .. code-block::

            play_sound <filename>[,volume]

    Script parameters:
        filename: Sound file to load.
        volume: Number between 0.0 and 1.0.

        Attention!
        The volume will be based on the main value
        in the options menu.
        e.g. if you set volume = 0.5 here, but the
        player has 0.5 among its options, then it'll
        result into 0.25 (0.5*0.5)

    """

    name = "play_sound"
    filename: str
    volume: Optional[float] = None

    def start(self) -> None:
        player = self.session.player
        _sound = prepare.SOUND_VOLUME
        sound_volume = float(player.game_variables.get("sound_volume", _sound))
        if not self.volume:
            volume = sound_volume
        else:
            lower, upper = prepare.SOUND_RANGE
            if lower <= self.volume <= upper:
                volume = self.volume * sound_volume
            else:
                raise ValueError(
                    f"{self.volume} must be between {lower} and {upper}",
                )
        sound = audio.load_sound(self.filename, volume)
        sound.play()
