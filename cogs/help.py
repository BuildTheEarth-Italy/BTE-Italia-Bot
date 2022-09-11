from typing import Optional
import discord
from discord.ext import commands
from discord.ext import menus
from discord import ui


class MyMenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=False):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.delete_message_after = delete_message_after

    async def start(self, ctx, *, channel=None, wait=False):
        # We wont be using wait/channel, you can implement them yourself. This is to match the MenuPages signature.
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        """This method calls ListPageSource.format_page class"""
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        """Only allow the author that invoke the command to be able to use the interaction"""
        return interaction.user == self.ctx.author

    @ui.button(emoji='◀', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction, button):
        self.stop_page.label = self.current_page
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @ui.button(label='1', style=discord.ButtonStyle.blurple)
    async def stop_page(self, interaction, button):
        await interaction.response.defer()

    @ui.button(emoji='▶', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction, button):
        self.stop_page.label = self.current_page+2

        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()



class HelpPageSource(menus.ListPageSource):
    def __init__(self, data, helpcommand, title, description):
        super().__init__(data, per_page=6)
        self.helpcommand = helpcommand
        self.title = title
        self.description = description

    def format_command_help(self, no, command):
        signature = self.helpcommand.get_command_signature(command)
        docs = self.helpcommand.get_command_brief(command)
        return f"{no}. {signature}\n{docs}"
    
    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        total_data = len(self.entries)
        embed = discord.Embed(title=self.title, description=self.description, color=discord.Color.blue())

        for name, value in entries:
            embed.add_field(name=name, value=value, inline=True)
        return embed



class MyHelp(commands.HelpCommand):

    def get_clean_command_signature(self, command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)


    async def send_bot_help(self, mapping):
        description="""
**If you need help with a category use:**
`£help [category]`
**If you need help with a command use:**
`£help [command]`
"""     
        entries=[]
        cogs = dict(self.context.bot.cogs)
        for k, v in cogs.items():
            entries.append([k, str([None if cogs[k].description == '' else cogs[k].description])])
        
        formatter = HelpPageSource(entries, self, title="❔ Help", description="**If you need help with a category use:**\n`£help [category]`\n**If you need help with a command use:**\n`£help [command]`")
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)


    async def send_cog_help(self, cog):
        commandlist = []
        filtered_commands=await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered_commands:
            signature=self.get_clean_command_signature(command)
            commandlist.append([str(signature), str(command.help)])

        
        formatter = HelpPageSource(commandlist, self, title="❔ Category help", description=str([None if cog.description == '' else cog.description]))
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)


    async def send_group_help(self, group):
        commandlist=[]
        filtered_commands=await self.filter_commands(group.commands, sort=True)
        for command in filtered_commands:
            commandlist.append([str(self.get_clean_command_signature(command)),str(command.help)])
        
        
        formatter = HelpPageSource(commandlist, self, title="❔ Command group help", description=str([None if group.description == '' else group.description]))
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)


    async def send_command_help(self, command):
        embed=discord.Embed(title=self.get_command_signature(command), description=command.help, colour=0xf2f2f2)
        
        await self.context.reply(embed=embed)
        



class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        help_command = MyHelp()
        help_command.cog = self
        bot.help_command = help_command


async def setup(bot):
    await bot.add_cog(Help(bot))