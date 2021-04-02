import discord, random, asyncio
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_voice_state_update')
    async def rickroll_voice(self, member, before, after):
        if before.channel != after.channel and after.channel is not None and member.bot is False:
            bot_member = member.guild.get_member(self.bot.user.id)
            if bot_member.permissions_in(after.channel).speak is False or bot_member.permissions_in(after.channel).connect is False:
                return
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('Files/rickroll.mp3'))
            try:
                await member.voice.channel.connect()
            except discord.errors.ClientException:
                pass
            try:
                await member.guild.voice_client.play(source)
            except TypeError:
                pass
            await asyncio.sleep(10)
            await member.guild.voice_client.disconnect()

    @commands.Cog.listener('on_message')
    async def rickroll_text(self, message):
        if message.guild is None or message.author.bot is True:
            return
        rickroll = False
        try:
            self.bot.rickroll[str(message.channel.id)] += 1
        except KeyError:
            self.bot.rickroll[str(message.channel.id)] = 1
        else:
            if self.bot.rickroll[str(message.channel.id)] >= 5:
                rickroll = True
        if rickroll is True:
            del self.bot.rickroll[str(message.channel.id)]
            option = random.choice(['video', 'gif', 'emoji', 'lyrics', 'youtube'])
            if option == 'video':
                file = discord.File("Files/rickroll.mp4")
                await message.reply(file=file, delete_after=45.0)
            elif option == 'gif':
                file = discord.File("Files/rickroll.gif")
                await message.reply(file=file, delete_after=45.0)
            elif option == 'emoji':
                await message.reply('<a:just_a_normal_blob_emoji:808436599330177024>', delete_after=45.0)
            elif option == 'lyrics':
                await message.reply("We're no strangers to love\nYou know the rules and so do I\nA full commitment's what I'm thinking of\nYou wouldn't get this from any other guy\nI just wanna tell you how I'm feeling\nGotta make you understand", delete_after=45.0)
            elif option == 'youtube':
                await message.reply('https://youtu.be/dQw4w9WgXcQ', delete_after=45.0)

def setup(bot):
    bot.add_cog(Misc(bot))
