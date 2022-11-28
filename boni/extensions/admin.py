import naff
from random import choice
from dotenv import get_key


class Admin(naff.Extension):
    def __init__(self, bot: naff.Client):
        self.bot: naff.Client = bot

    admin_cmd = naff.SlashCommand(
        name="admin",
        description="Admin commands",
        default_member_permissions=naff.Permissions.ADMINISTRATOR,
        dm_permission=False,
    )

    @admin_cmd.subcommand(
        sub_cmd_name="post_rules", sub_cmd_description="Post rules to channel"
    )
    @naff.slash_option(
        name="channel",
        description="Channel to post rules to",
        opt_type=naff.OptionTypes.CHANNEL,
        channel_types=[naff.ChannelTypes.GUILD_TEXT],
        required=True,
    )
    async def post_rules(
        self, ctx: naff.InteractionContext, channel: naff.GuildText
    ) -> None:
        welcome = "What The Slambonis are about isn't hard to understand. Yes, we game together, but we're focused on hanging out and having fun. We don't have skill/rank/level requirements for any games we play, and we never will. However, we take new memberships pretty seriously. We're a small group that takes pride in taking time to curate members who will help keep our community chill, healthy, and active. That being said, we believe you would be a valuable part of The Slambonis. We can't wait to get you on the path of \"slammin' with the fam!\"\n\n\u200b"

        rules_embeds = [
            naff.Embed(
                title="😍 Treat on another with love and respect",
                description="No one likes a jerk. Keep the chat clean and don't be using slurs/insults or any other form of harassment. We're all here to have fun, and we're all here to be ourselves.",
                color="#1e99d7",
            ),
            naff.Embed(
                title="🔞 Keep it PG-18",
                description="No porn, no gore, and no fucked up videos. We are all for the memes, but watch what you post.",
                color="#1e99d7",
            ),
            naff.Embed(
                title="🧌 No trolling",
                description="Dont join just to cause a ruckus. We're here to get away from all that jazz.",
                color="#1e99d7",
            ),
            naff.Embed(
                title="📵 No DM Harassment",
                description="Do not DM someone without their permission and do not harrass them. (If you are being harassed, please report it to a moderator.)",
                color="#1e99d7",
            ),
            naff.Embed(
                title="📢 No Promoting",
                description="Don't come in here to then just post your links without being an active member. We are ok with people sharing cool clips they get in game, but not just posting them and never being active.",
                color="#1e99d7",
            ),
            naff.Embed(
                title="👮 Follow Discord TOS",
                description="It is required that you follow [Discord's TOS](<https://discord.com/terms>).",
                color="#1e99d7",
            ),
            naff.Embed(
                title="ℹ️ One more thing...",
                description="We take the time to really curate our members so you will gain a recruitment role for about 1-2 weeks (depending on activity) to help us get to know you and vice versa. This will help us learn if we are a good fit together!",
                color="#1e99d7",
            ),
        ]
        button = naff.Button(
            naff.ButtonStyles.BLUE, label="I agree to these rules", custom_id="rules"
        )
        await channel.send(content=welcome, embeds=rules_embeds, components=button)
        await ctx.send("Sent to: " + channel.mention, ephemeral=True)

    @naff.listen(naff.events.ButtonPressed)
    async def toggle_accepted_rules(self, event: naff.events.ButtonPressed) -> None:
        ctx = event.ctx
        recruitment_role = await ctx.guild.fetch_role(
            int(get_key(".env", "RECRUIT_ROLE"))
        )
        slamboni_role = await ctx.guild.fetch_role(int(get_key(".env", "SLAM_ROLE")))
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


def setup(bot: naff.Client):
    Admin(bot)
