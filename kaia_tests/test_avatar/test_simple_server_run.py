from kaia.avatar import AvatarTestApi, AvatarSettings
from kaia.narrator import SimpleNarrator, World
from unittest import TestCase

class AvatarTestCase(TestCase):
    def test_avatar(self):
        with AvatarTestApi(AvatarSettings(),) as api:
            api.state_change({World.character.field_name:'character_1', 'test':'value'})
            state = api.state_get()
            self.assertDictEqual(
                dict(character='character_1', test='value'),
                state
            )