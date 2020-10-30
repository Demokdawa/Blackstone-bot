# !rcheck to get status of the image-serving service
@check_cog_redditscrap()
@commands.command()
async def rcheck(self, ctx):
    if rdy == 0:
        await ctx.channel.send("Je démarre gros, 2 sec 😎 ({} / {})".format(progress, len(sub_dict)))
    elif rdy == 1:
        await ctx.channel.send("Je suis la pour toi mon chou ❤")


# Decorator to check if reddit bot is ready to serve
def check_if_bot_rdy():
    async def predicate(ctx):
        if rdy == 0:
            await ctx.channel.send("Je suis encore en train de fouiller le web, patiente quelques minutes 😎 ({} / {}) "
                                   .format(progress, len(sub_dict)))

        elif rdy == 1:
            return True

    return commands.check(predicate)

sub_dict = db_get_reddit_sub_dict()  # [dict] with subs (dict key is sub)

