  
'''
using discord.py version 1.0.0a
'''
import discord
import asyncio
import re
import random
import datetime
import multiprocessing
import threading
import concurrent

#BOT_OWNER_ROLE = 'Runner' # change to what you need
#BOT_OWNER_ROLE_ID = "503197827556704268" 
  
g="https://discord.gg/rsQUHwq" 

 
oot_channel_id_list = ["842239797803876372", #trivia-x
"840653201618632704", #challenge
"842267116677890049", #legit
#"835201293600817212", #text
#"", #duck
#"837133178031964190", #mohit
#"728281366919118918", #unt
#HQ
#"570794448808837131", #swag iq king
#"821538954858987541", #sivam
#"822757211222179851", #anurag
#"822084276265812029", #mohit
#"816481662615027764", #legit
#"773602512812769331", #drogen
#"756213988986978539", #harsit
#swag iq
#"773390146406055937", #galaxy
#"756445815001710632", #harsit
#"570794448808837131", #swag iq king
#"770566217894461500", #anurag
#"774480600010457108", #ukt
#"772056500217577515", #google
#"773602513597235231", #drogen
#"770566217894461500", #Anurag 
#moolah
#"773887678722211860", #galaxy
#"770655464094564402", #anurag
#"765159847586955285", #drogen
#"772860624437772338", #harsit
#"774480643957981226", #ukt
#"718928611356180531", #x trivia
#"740237583791030312", #nation
#"733232241680973855", #google 
#"739125037478576139", #risy
#"728282103480975462",
#"729900288361627771",
#"728998207949897808",
#"737572429353975869",
#"741126316392317010", #mind
#"735912993706999959", #nation SwagIQ 
#"733413471483330601", #mayur
#"732405971611287552", #glxy
#"736889487761735732", #savage 
#"736042800650387517", #anurag
#"725619546161152042", #pride
#"731059312927178752", #smart
#"740581485462945894", #velocity 
#"736950547034275862", #magic
#"734734974594318366", #allen
#"740581485462945894", #velocity 
#"739123364827758593", #pride
#"813078905308708904", #trivia x answer channel
"842238599620460577"  #private
]
answer_pattern = re.compile(r'(not|n)?([1-3]{1})(\?)?(cnf)?(\?)?$', re.IGNORECASE)

apgscore = 480
nomarkscore = 180
markscore = 90

async def update_scores(content, answer_scores):
    global answer_pattern

    m = answer_pattern.match(content)
    if m is None:
        return False

    ind = int(m[2])-1

    if m[1] is None:
        if m[3] is None:
            if m[4] is None:
                answer_scores[ind] += nomarkscore
            else: # apg
                if m[5] is None:
                    answer_scores[ind] += apgscore
                else:
                    answer_scores[ind] += markscore

        else: # 1? ...
            answer_scores[ind] += markscore

    else: # contains not or n
        if m[3] is None:
            answer_scores[ind] -= nomarkscore
        else:
            answer_scores[ind] -= markscore

    return True

class SelfBot(discord.Client):

    def __init__(self, update_event, answer_scores):
        super().__init__()
        global oot_channel_id_list
        #global wrong
        self.oot_channel_id_list = oot_channel_id_list
        self.update_event = update_event
        self.answer_scores = answer_scores

    async def on_ready(self):
        print("======================")
        print("Trivia X")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))

    # @bot.event
    # async def on_message(message):
    #    if message.content.startswith('-debug'):
    #         await message.channel.send('d')

        def is_scores_updated(message):
            if message.guild == None or \
                str(message.channel.id) not in self.oot_channel_id_list:
                return False

            content = message.content.replace(' ', '').replace("'", "")
            m = answer_pattern.match(content)
            if m is None:
                return False

            ind = int(m[2])-1

            if m[1] is None:
                if m[3] is None:
                    if m[4] is None:
                        self.answer_scores[ind] += nomarkscore
                    else: # apg
                        if m[5] is None:
                            self.answer_scores[ind] += apgscore
                        else:
                            self.answer_scores[ind] += markscore

                else: # 1? ...
                    self.answer_scores[ind] += markscore

            else: # contains not or n
                if m[3] is None:
                    self.answer_scores[ind] -= nomarkscore
                else:
                    self.answer_scores[ind] -= markscore

            return True

        while True:
            await self.wait_for('message', check=is_scores_updated)
            self.update_event.set()

class Bot(discord.Client):

    def __init__(self, answer_scores):
        super().__init__()
        self.bot_channel_id_list = []
        self.embed_msg = None
        self.embed_channel_id = None
        #global wrong
        self.answer_scores = answer_scores

        # embed creation
        value=random.randint(0,0xffffff)
        self.embed=discord.Embed(title="",description =f" ",colour=value)
        self.embed.add_field(name="**__Option ❶__**", value=f"<a:emoji_57:726335239902986263> Crowd `:` **[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❷__**", value=f"<a:emoji_57:726335239902986263> Crowd `:` **[0]({g})**", inline=False)
        self.embed.add_field(name="**__Option ❸__**", value=f"<a:emoji_57:726335239902986263> Crowd `:` **[0]({g})**", inline=False)
        #self.embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/716879425655799858/745718978214625410/726164501543518278.gif")
        self.embed.set_footer(text='Nitin',icon_url='')
        self.embed.timestamp = (datetime.datetime.utcnow())
        #self.embed.add_field(name="**__Correct Answer__**", value="0", inline=False)
       # self.embed.add_field(name="**__Not Answer__**", value="0", inline=False) 


        #await self.bot.add_reaction(embed,':spy:')


    async def clear_results(self):
        for i in range(len(self.answer_scores)):
            self.answer_scores[i]=0

    async def update_embeds(self):
      #  global wrong

         

        one_check = ""
        two_check = ""
        three_check = ""
        mark_check_one=""
        mark_check_two=""
        mark_check_three=""
        one_cross =""
        two_cross =""
        three_cross =""
        #best_answer = "** **   **`Fetching ...`** ** **"
        #erased_answer = "** **  **`Erasing ...` ** ** **"
              

        lst_scores = list(self.answer_scores)
        

        highest = max(lst_scores)
        gif_ans = 'https://cdn.discordapp.com/attachments/716879425655799858/745718978214625410/726164501543518278.gif'
        #best_answer = 'Loading'
        lowest = min(lst_scores)
        answer = lst_scores.index(highest)+1
        wrong = lst_scores.index(lowest)+1
       #global wrong             

        if highest > 0:
            if answer == 1:
                one_check = " ✅  "
                mark_check_one = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/attachments/716879425655799858/742730340744822864/723415445167931452.png"
                #best_answer = "** ** **Answer :** :one: = ✅"
                   
            else:
                one_check = " "

            if answer == 2:
                two_check = " ✅  "
                mark_check_two = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/attachments/716879425655799858/742730400706854972/723416002666299433.png"
                #best_answer = "** ** **Answer :** :two: = ✅"
                   
            else:
                two_check = ""

            if answer == 3:
                three_check = " ✅  "
                mark_check_three = "<:emoji_62:735102374523306047>"
                gif_ans = "https://cdn.discordapp.com/attachments/716879425655799858/742730625647247501/723418348834258974.png"
                #best_answer = "** ** **Answer :** :three: = ✅"
                   
            else:
                three_check = ""

            

        if lowest < 0:
            if wrong == 1:
                one_cross = "❌"
                #erased_answer = "❌ :one: = ❌ " 
               
            if wrong == 2:
                two_cross = "❌"
                #erased_answer = "<a:emoji_53:721389606712377505> :two: = ❌" 
               
            if wrong == 3:
                three_cross = "❌"
                #erased_answer = "<a:emoji_53:721389606712377505> :three: = ❌"
         
    
        self.embed.set_field_at(0, name="**__Option ❶__**", value=f"**[{lst_scores[0]}]({g}){one_check}{one_cross}**")
        self.embed.set_field_at(1, name="**__Option ❷__**", value=f"**[{lst_scores[1]}]({g}){two_check}{two_cross}**")
        self.embed.set_field_at(2, name="**__Option ❸__**", value=f"**[{lst_scores[2]}]({g}){three_check}{three_cross}**")
        #self.embed.set_thumbnail(url="{}".format(gif_ans))
        self.embed.set_footer(text='Swag-iq',icon_url='' )
        self.embed.timestamp = (datetime.datetime.utcnow())
       # self.embed.set_field_at(3, name="**__Correct Answer__**", value=f"**[{confirm}]({g}) {right_answer}**", inline=True)
      #  self.embed.set_field_at(4, name="**__Not Answer__**", value=f"**[{uncnf}]({g}) {not_answer}**", inline=True) 


        if self.embed_msg is not None:
            await self.embed_msg.edit(embed=self.embed)

    async def on_ready(self):
        print("==============")
        print("Trivia X")
        print("Connected to discord.")
        print("User: " + self.user.name)
        print("ID: " + str(self.user.id))
        log=self.get_channel(841339755294883874)
        await log.send("> **Swag-iq Bot Is Updated ** ✅")
        await self.clear_results()
        await self.update_embeds()
        #await self.change_presence(activity=discord.Game(name='with '+str(len(set(self.get_all_members())))+' users'))
        await self.change_presence(activity=discord.Activity(type=1,name="With Swag-iq"))

    async def on_message(self, message):


        # if message is private
        if message.author == self.user or message.guild == None:
            return

        if message.content.lower() == "s":
            await message.delete()

            self.embed_msg = None
            await self.clear_results()
            await self.update_embeds()
            self.embed_msg = \
                await message.channel.send('',embed=self.embed)
            #await self.embed_msg.add_reaction("🎉")
            #await self.embed_msg.add_reaction("💯")
            #await self.embed_msg.add_reaction("🧡")
            self.embed_channel_id = message.channel.id    
            

         
        if message.content.lower() == "run":
          await message.delete()
          if BOT_OWNER_ROLE in [role.name for role in message.author.roles]:
              embed = discord.Embed(title="**__Next Game : Loco Vedantu__ = {Prize Money : 15000Rs.}**", color=0x0FF14)
              await message.channel.send(embed=embed)
          

        # process votes
        if message.channel.id == self.embed_channel_id:
            content = message.content.replace(' ', '').replace("'", "")
            updated = await update_scores(content, self.answer_scores)
            if updated:
                await self.update_embeds()

def bot_with_cyclic_update_process(update_event, answer_scores):

    def cyclic_update(bot, update_event):
        f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
        while True:
            update_event.wait()
            update_event.clear()
            f.cancel()
            f = asyncio.run_coroutine_threadsafe(bot.update_embeds(), bot.loop)
            #res = f.result()

    bot = Bot(answer_scores)

    upd_thread = threading.Thread(target=cyclic_update, args=(bot, update_event))
    upd_thread.start()

    loop = asyncio.get_event_loop()
    loop.create_task(bot.start('ODQyNDk5NDU0MjAzNDYxNjQy.YJ2Mwg.A6Mq8KkC2UBmZSaCLGm4CkZACBE'))
    loop.run_forever()


def selfbot_process(update_event, answer_scores):

    selfbot = SelfBot(update_event, answer_scores)

    loop = asyncio.get_event_loop()
    loop.create_task(selfbot.start('ODM5MjYzMTMwMTAyMDA1Nzc5.YJHGsg.KjoWDNZyeDsRXRNPigsE2yztSeU',
                                   bot=True))
    loop.run_forever()

if __name__ == '__main__':

    # running bot and selfbot in separate OS processes

    # shared event for embed update
    update_event = multiprocessing.Event()

    # shared array with answer results
    answer_scores = multiprocessing.Array(typecode_or_type='i', size_or_initializer=5)

    p_bot = multiprocessing.Process(target=bot_with_cyclic_update_process, args=(update_event, answer_scores))
    p_selfbot = multiprocessing.Process(target=selfbot_process, args=(update_event, answer_scores))

    p_bot.start()
    p_selfbot.start()

    p_bot.join()
    p_selfbot.join()




 
 
