import discord
from discord.ext import commands

intents = discord.Intents.default()

intents.members = True

client = commands.Bot(command_prefix=">", intents = intents) #prefisso per usare i comandi

client.remove_command("help")

f = open("regole.txt","r") #Lista delle regole e funzione per leggerle da file esterno
regole = f.readlines()

parole = ["cane","gatto"] #Lista parole vietate

@client.event #Messaggio di stato
async def on_ready():
    print("Il Bot è pronto")

@client.event #Elimina il messaggio se una parola è presente enlla lista parle vietate
async def on_message(msg):
    for word in parole:
        if word in msg.content:
            await msg.delete()

    await client.process_commands(msg)

@client.event #Gestione degli errori
async def on_command_error(ctx,error,):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("non hai i permessi per usare questo comando, contatta un amministratore se necessario.")
        await ctx.message.delete()
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("mancano alcuni parametri per l'esecuzione corretta del comando, controlla e riprova.")
        await ctx.message.delete()
    elif isinstance(error,commands.BadArgument):
        await ctx.send("i parametri fortini non sono della tipologia giusta, controlla e riprova.")
        await ctx.message.delete()
    else:
        raise error

@client.command() #test
async def ping(ctx):
    await ctx.send("pong")

@client.command(aliases=["regole","rule","rules"]) #Ritorna le regole
async def regola(ctx,*,number):
    await ctx.send(regole[int(number)-1])

@client.command(aliases=["c"]) #Cancella tot ultimi messaggi, se non metti quanti, di default sono gli ultimi 2
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)
    
@client.command(aliases=["k"]) #Comando kick
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "motivo non specificato"):
    try:
        await member.send("Sei stato kickato dal server perchè:" +reason)
    except:
        await ctx.send("Il utente ha i messaggi bloccati, impossibile notificare il kick.")
    await ctx.send(member.name + " e' stato trollato perchè: "+reason)
    await member.kick(reason=reason)

@client.command(aliases=["b"]) #Comando ban
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason= "motivo non specificato"):
    await ctx.send(member.name + " e' stato cringelollato perchè: "+reason)
    await member.ban(reason=reason)

@client.command(aliases = ["ub", "sbanna"]) #Comando unban
@commands.has_permissions(ban_members = True)
async def unban(ctx,*,member): #!unban nomeutente#codice
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name,member_disc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " e' stato riammesso tra il popolo eletto!")
            return
    await ctx.send(member + " non e' stato trovato")

@client.command(aliases=["m","zitto","muta"]) #Comando mute
@commands.has_permissions(kick_members = True)
async def mute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(794306598834012171)

    await member.add_roles(muted_role)
    await ctx.send(member.mention + " sei stato mutato! :mute:")

@client.command(aliases = ["user","info"])
@commands.has_permissions(kick_members = True)
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title = member.display_name, description = member.mention, color = discord.Colour.purple())
    embed.add_field(name= "ID", value = member.id, inline = True)
    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url= ctx.author.avatar_url, text = f"Richiesto da {ctx.author.name}")
    await ctx.send(embed = embed)

@client.command(aliases = ["smuta"]) #Comando unmute
@commands.has_permissions(kick_members = True)
async def unmute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(794306598834012171)

    await member.remove_roles(muted_role)
    await ctx.send(member.mention + " sei stato smutato!")

@client.command(aliases = ["pl","quest"]) #Creare sondaggi
@commands.has_permissions(kick_members = True)
async def poll(ctx,*,msg):
    channel = ctx.channel
    try:
        op1, op2 = msg.split(" o ")
        txt = f"Metti la reazione :one: per {op1}, :two: per {op2}"
    except:
        await channel.send("La corretta sintassi è: !poll scelta1 o scelta 2")
        return


    embed = discord.Embed(title="Sondaggio", description = txt, colour = discord.Colour.purple())
    message_ = await channel.send(embed=embed)
    await message_.add_reaction("1️⃣")
    await message_.add_reaction("2️⃣")
    await ctx.message.delete()

@client.group(invoke_without_command = True) #Comando help personalizzato
async def help(ctx):
    embed=discord.Embed(title="Lista e info comandi", description="Usa >help <comando> per avere ulteriori informazioni su un preciso comando")
    embed.set_author(name="Galoppino_Bot™️", icon_url="https://www.altovicentinonline.it/wp-content/uploads/2018/10/asino.jpg")
    embed.set_thumbnail(url="https://multiculturalmarriage.files.wordpress.com/2013/07/help-button-hi.png")
    embed.add_field(name="Moderazione ", value="kick, ban, unban, warn, clear, mute, unmute, poll, whois", inline=True)
    embed.add_field(name="Info e giochi", value="8ball, reverse, regola", inline=True)
    embed.set_footer(text="Il Bot è stato offerto dalla... diciamo non Fininvest, non La7, non Sky... l'altra. E ci siamo capiti.")
    await ctx.send(embed=embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def kick(ctx):
    embed=discord.Embed(title= "Kick", description= "caccia un utente dal server, non serve specificare necessariamente il motivo")
    embed.set_author(name= "Galoppino_Bot™️", icon_url= "https://www.altovicentinonline.it/wp-content/uploads/2018/10/asino.jpg")
    embed.set_thumbnail(url= "https://png2.cleanpng.com/sh/6f1bb6037a041e2de1bae6edc6adb84a/L0KzQYm3VMA2N6dnj5H0aYP2gLBuTfZtgZpzf590aXPuPbf2jCRjaZ1xRdlqbXWwgsb1jvlvb15yedC2NXHmRbe4gcVjOZY8TqY3N0G3RIaBVMkyPWM3UaQ6OEm2R4OBV75xdpg=/kisspng-flying-kick-football-game-running-man-5ac5f1a5b1e764.7144584915229218937287.png")
    embed.add_field(name= "Sintassi", value= ">kick <@utente> <motivo>", inline=True)
    embed.set_footer(text= "Il Bot è stato offerto dalla... diciamo non Fininvest, non La7, non Sky... l'altra. E ci siamo capiti.")
    await ctx.send(embed=embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def ban(ctx):
    embed = discord.Embed(title ="Ban", description = "Banna un utente dal server, non serve specificare necessariamente il motivo", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">Ban <nome_utente> [motivo]")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def unban(ctx):
    embed = discord.Embed(title ="Unban", description = "Sbanna un utente dal server, es. nome#tag", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">unban <nome_utente#tag")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def clear(ctx):
    embed = discord.Embed(title ="Clear", description = "Cancella tot messaggi dalla chat, se non specifichi quanti cancella gli ultimi 2", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">clear <numero_messaggi>")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def mute(ctx):
    embed = discord.Embed(title ="Mute", description = "Muta nei canali vocali l'utente selezionato", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">mute <nome_utente>")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def unmute(ctx):
    embed = discord.Embed(title ="unmute", description = "smuta l'utente selezionato", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">unmute <nome_utente>")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def poll(ctx):
    embed = discord.Embed(title ="Poll", description = "crea un sondaggio tra due opzioni", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">poll <opzione1> o <opzione2>")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
@commands.has_permissions(kick_members = True)
async def whois(ctx):
    embed = discord.Embed(title ="WhoIs", description = "mostra le informazioni di un utente", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">whois <nome_utente>")

    await ctx.send(embed = embed)

@help.command() #Descrizione del comando kick
async def regola(ctx):
    embed = discord.Embed(title ="Regola", description = "mostra la regola corrispondente al numero richiesto tra 1-7", color = discord.Color.purple())
    embed.add_field(name = "**Sintassi**", value = ">regola <numero_regola>")

    await ctx.send(embed = embed)

client.run("NzkzMTY4OTg5MTMxMTEyNDQ4.X-oWLw.im7Xr0a1Io9nC1QUptTHNXbwAlQ") #Qua va inserito il token del bot