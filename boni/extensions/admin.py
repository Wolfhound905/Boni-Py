from interactions import (
    Activity,
    Button,
    ComponentContext,
    Extension,
    Client,
    SlashCommand,
    Permissions,
    GuildText,
    SlashContext,
    StringSelectMenu,
    StringSelectOption,
    slash_option,
    OptionType,
    ChannelType,
    Embed,
    listen,
    events,
)
from random import choice
from dotenv import get_key
from boni.utils.logging import logger

from boni.utils.config import load_config

config = load_config()


class Admin(Extension):
    def __init__(self, bot: Client):
        self.bot: Client = bot

        self.platform_roles = {
            "switch": config.roles.switch,
            "playstation": config.roles.playstation,
            "xbox": config.roles.xbox,
            "pc": config.roles.pc,
        }

        self.game_roles = {
            "rocketleague": config.roles.rocket_league,
            "fortnite": config.roles.fortnite,
            "minecraft": config.roles.minecraft,
            "huntshowdown": config.roles.hunt_showdown,
        }

        self.region_roles = {
            "uswest": config.roles.us_west,
            "uscentral": config.roles.us_central,
            "useast": config.roles.us_east,
            "eu": config.roles.eu,
            "asia": config.roles.asia,
        }

    admin_cmd = SlashCommand(
        name="admin",
        description="Admin commands",
        default_member_permissions=Permissions.ADMINISTRATOR,
        dm_permission=False,
    )

    @admin_cmd.subcommand(
        sub_cmd_name="rules",
        sub_cmd_description="Post rules to channel",
        group_name="post",
    )
    @slash_option(
        name="channel",
        description="Channel to post rules to",
        opt_type=OptionType.CHANNEL,
        channel_types=[ChannelType.GUILD_TEXT],
        required=True,
    )
    async def post_rules(self, ctx: SlashContext, channel: GuildText) -> None:
        welcome = "What The Slambonis are about isn't hard to understand. Yes, we game together, but we're focused on hanging out and having fun. We don't have skill/rank/level requirements for any games we play, and we never will. However, we take new memberships pretty seriously. We're a small group that takes pride in taking time to curate members who will help keep our community chill, healthy, and active. That being said, we believe you would be a valuable part of The Slambonis. We can't wait to get you on the path of \"slammin' with the fam!\"\n\n\u200b"

        rules_embeds = [
            Embed(
                title="😍 Treat one another with love and respect",
                description="No one likes a jerk. Keep the chat clean and don't be using slurs/insults or any other form of harassment. We're all here to have fun, and we're all here to be ourselves.",
                color="#1e99d7",
            ),
            Embed(
                title="🔞 Keep it PG-18",
                description="No porn, no gore, and no fucked up videos. We are all for the memes, but watch what you post.",
                color="#1e99d7",
            ),
            Embed(
                title="🧌 No trolling",
                description="Dont join just to cause a ruckus. We're here to get away from all that jazz.",
                color="#1e99d7",
            ),
            Embed(
                title="📵 No DM Harassment",
                description="Do not DM someone without their permission and do not harrass them. (If you are being harassed, please report it to a moderator.)",
                color="#1e99d7",
            ),
            Embed(
                title="📢 No Promoting",
                description="Don't come in here to then just post your links without being an active member. We are ok with people sharing cool clips they get in game, but not just posting them and never being active.",
                color="#1e99d7",
            ),
            Embed(
                title="👮 Follow Discord TOS",
                description="It is required that you follow [Discord's TOS](<https://discord.com/terms>).",
                color="#1e99d7",
            ),
            Embed(
                title="ℹ️ One more thing...",
                description="We take the time to really curate our members so you will gain a recruitment role for about 1-2 weeks (depending on activity) to help us get to know you and vice versa. This will help us learn if we are a good fit together!",
                color="#1e99d7",
            ),
        ]
        button = Button(
            style=Button.Styles.BLUE, label="I agree to these rules", custom_id="rules"
        )
        await channel.send(content=welcome, embeds=rules_embeds, components=button)
        await ctx.send("Sent to: " + channel.mention, ephemeral=True)

    @listen(events.ButtonPressed)
    async def toggle_accepted_rules(self, event: events.ButtonPressed) -> None:
        ctx = event.ctx
        if ctx.custom_id != "rules":
            return

        recruitment_role = await ctx.guild.fetch_role(config.roles.recruit)
        slamboni_role = await ctx.guild.fetch_role(config.roles.slam)
        if (
            recruitment_role not in ctx.author.roles
            and slamboni_role not in ctx.author.roles
        ):
            await ctx.author.add_role(recruitment_role)
            await ctx.edit_origin()
        elif slamboni_role in ctx.author.roles:
            await ctx.send(
                "Since you're already a Slamboni, you don't need to accept the rules again.",
                ephemeral=True,
            )
        else:
            await ctx.author.remove_role(recruitment_role)
            await ctx.edit_origin()

    @admin_cmd.subcommand(
        sub_cmd_name="roles",
        sub_cmd_description="Post manage roles message",
        group_name="post",
    )
    @slash_option(
        name="channel",
        description="Channel to post roles to",
        opt_type=OptionType.CHANNEL,
        channel_types=[ChannelType.GUILD_TEXT],
        required=True,
    )
    async def post_roles(self, ctx: SlashContext, channel: GuildText) -> None:
        content = "Welcome to the locker room! Go ahead and grab your gear and get ready to play some games. We have a few roles you can add to yourself to help us get to know you better. If you have any questions, feel free to ask a moderator or admin. We're here to help!\n\n\u200b"

        switch = StringSelectMenu(
            StringSelectOption(
                label="PC",
                value="pc",
                emoji="<:pc:1046642402850517012>",
            ),
            StringSelectOption(
                label="Xbox",
                value="xbox",
                emoji="<:xbox:1046634053840941106>",
            ),
            StringSelectOption(
                label="Playstation",
                value="playstation",
                emoji="<:playstation:1046634875677048842>",
            ),
            StringSelectOption(
                label="Switch",
                value="switch",
                emoji="<:nintendo:1046634892940812348>",
            ),
            placeholder="Select your platform(s)",
            min_values=1,
            max_values=4,
            custom_id="platform_select",
        )

        games = StringSelectMenu(
            StringSelectOption(
                label="Fortnite",
                value="fortnite",
                emoji="<:fortnite:1046642116186619997>",
            ),
            StringSelectOption(
                label="Hunt Showdown",
                value="huntshowdown",
                emoji="<:huntshowdown:1046642115171590177>",
            ),
            StringSelectOption(
                label="Minecraft",
                value="minecraft",
                emoji="<:minecraft:1046642117390372924>",
            ),
            StringSelectOption(
                label="Rocket League",
                value="rocketleague",
                emoji="<:rocketleague:1046642118300545114>",
            ),
            placeholder="Select your game(s)",
            min_values=1,
            max_values=4,
            custom_id="game_select",
        )

        regions = StringSelectMenu(
            StringSelectOption(
                label="US West",
                value="uswest",
            ),
            StringSelectOption(
                label="US Central",
                value="uscentral",
            ),
            StringSelectOption(
                label="US East",
                value="useast",
            ),
            StringSelectOption(
                label="Europe",
                value="eu",
            ),
            StringSelectOption(
                label="Asia",
                value="asia",
            ),
            placeholder="Select your region",
            min_values=1,
            max_values=1,
            custom_id="region_select",
        )

        await channel.send(
            content=content,
            components=[[switch], [games], [regions]],
        )
        await ctx.send("Sent to: " + channel.mention, ephemeral=True)

    async def toggle_custom_roles(self, ctx: ComponentContext, roles: dict):
        _roles = roles

        local_author_roles = [role.id for role in ctx.author.roles]

        for role in _roles.values():
            if role in local_author_roles:
                local_author_roles.remove(role)

        for role in ctx.values:
            local_author_roles.append(_roles[role])

        await ctx.author.edit(roles=local_author_roles)
        await ctx.send("Roles updated!", ephemeral=True)

    @listen(events.Select)
    async def toggle_roles(self, event: events.Select):
        ctx = event.ctx
        if ctx.custom_id == "platform_select":
            await self.toggle_custom_roles(ctx, self.platform_roles)
        elif ctx.custom_id == "game_select":
            await self.toggle_custom_roles(ctx, self.game_roles)
        elif ctx.custom_id == "region_select":
            await self.toggle_custom_roles(ctx, self.region_roles)

    @listen(events.Startup)
    async def startup(self) -> None:
        logger.info("Online")


def setup(bot: Client):
    Admin(bot)
