from app.FollowBot import Bot
import asyncio


bot = Bot()

if __name__ == '__main__':
    asyncio.run(bot.main_loop())
