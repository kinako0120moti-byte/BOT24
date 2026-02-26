import discord
from discord import app_commands
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# =========================
# 🎭 セリフデータ
# =========================

LINES = {
    "ツンデレ": {
        "N": [
            "べ、別に{target}くんのためじゃないし！",
            "{target}くんが困ってるなら仕方なくよ？"
        ],
        "R": [
            "{target}くんと一緒なら…悪くないかも。",
        ],
        "SR": [
            "ほんとは…{target}くんのこと気になってるの。",
        ],
        "SSR": [
            "だ、大好きなんだから…勘違いしないでよね！"
        ],
        "UR": [
            "ほんとは毎日{target}くんのこと考えてるの…恥ずかしい…"
        ]
    },
    "元気": {
        "N": [
            "{target}くん！今日もがんばろー！",
            "えへへ！{target}くん見つけた！"
        ],
        "R": [
            "{target}くんといると楽しい！",
        ],
        "SR": [
            "もっと一緒にいたいな〜！",
        ],
        "SSR": [
            "{target}くん大好きー！！"
        ],
        "UR": [
            "ぎゅーしてもいい？だめ？恥ずかしい〜！"
        ]
    }
}

# =========================
# 🎲 ガチャ確率
# =========================

def roll_rarity():
    r = random.random()
    if r < 0.01:
        return "UR"
    elif r < 0.05:
        return "SSR"
    elif r < 0.15:
        return "SR"
    elif r < 0.40:
        return "R"
    else:
        return "N"

# =========================
# 📝 名前入力モーダル
# =========================

class NameModal(discord.ui.Modal, title="名前を入力してね！"):
    target_name = discord.ui.TextInput(label="呼びたい名前（例：太郎）")

    def __init__(self, character):
        super().__init__()
        self.character = character

    async def on_submit(self, interaction: discord.Interaction):
        rarity = roll_rarity()
        line = random.choice(LINES[self.character][rarity])
        final_line = line.format(target=self.target_name.value)

        color = discord.Color.green()
        if rarity == "SR":
            color = discord.Color.blue()
        elif rarity == "SSR":
            color = discord.Color.purple()
        elif rarity == "UR":
            color = discord.Color.gold()

        embed = discord.Embed(
            title=f"🎲 レア度: {rarity}",
            description=f"💬 {final_line}",
            color=color
        )

        await interaction.response.send_message(embed=embed)

# =========================
# 🔘 キャラ選択ボタン
# =========================

class CharacterView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.button(label="ツンデレ", style=discord.ButtonStyle.primary)
    async def tsundere(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("ツンデレ"))

    @discord.ui.button(label="元気", style=discord.ButtonStyle.success)
    async def genki(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("元気"))

# =========================
# 🚀 スラッシュコマンド
# =========================

@bot.tree.command(name="serifu", description="セリフガチャを引く！")
async def serifu(interaction: discord.Interaction):
    await interaction.response.send_message(
        "キャラを選んでね！",
        view=CharacterView()
    )

# =========================
# 起動時
# =========================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"ログインしました: {bot.user}")

bot.run(TOKEN)