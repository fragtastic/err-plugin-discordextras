from errbot import BotPlugin, botcmd, webhook
from bottle import redirect


# https://discordapi.com/permissions.html
DISCORD_PERMISSIONS = 1275591745
MEME_BASE = '../memes'

class DiscordAddon(BotPlugin):
    """This is plugin for additional Discord specific functions."""

    def activate(self):
        """Method runs when plugin is loaded."""
        if self._bot.mode != 'discord':
            # TODO - logging during activate() doesn't seem to work
            self.log.warning('Discord backend must be active for this plugin to load.')
            return 
        super().activate()

    @webhook('/discord/invite')
    def invitehook(self, incoming_request):
        """Webhook that returns a Discord invitation link."""
        return redirect(f"{self.getoauthlink()}")

    @botcmd
    def invite(self, msg, args):
        """Returns a Discord invitation link."""
        return f"Invite me to your Discord server: {self.getoauthlink()}"

    @botcmd
    def setplaying(self, msg, args):
        """Changes the currently playing game."""
        self._bot.change_presence(None, f'{args}')

    @botcmd
    def showid(self, msg, args):
        """Execute to get ID of bot."""
        return self.getid()

    @botcmd
    def checkdiscord(self, msg, args):
        """Testing command, replies if the bot is in Discord mode."""
        if self._bot.mode == "discord":
            return 'Discord mode'
        return 'Not Discord mode'

    @botcmd
    def getrandommeme(self, msg, args):
        """Sends a random file from the meme directory."""
        self.log.debug('Choosing random meme')
        import os
        import random
        meme = random.choice(os.listdir(self.meme_base))
        self.log.debug('Chose meme %s' % meme)
        self.getmeme(msg, meme)

    @botcmd
    def getmeme(self, msg, args):
        """Sends a file from the meme directory."""
        self.log.debug('Uploading meme to %s' % msg)
        import ntpath
        self._bot.upload_file(msg, '%s/%s' % (self.meme_base, ntpath.basename(str(args))))

    def getid(self):
        """Helper to get the client ID of the bot."""
        return self._bot.client.user.id

    def getoauthlink(self):
        """Returns a Discord invidation link with permissions."""
        return f"https://discordapp.com/oauth2/authorize?client_id={self.getid()}&scope=bot" \
        "&permissions={DISCORD_PERMISSIONS}"
