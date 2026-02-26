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
            "{target}くんが困ってるなら仕方なくよ？",
            "勘違いしないでよね！",
            "暇だったから来ただけよ。"
        ],
        "R": [
            "{target}くんと一緒なら…悪くないかも。",
            "少しくらいなら、隣にいてあげてもいいわよ。",
            "…今日は特別だからね？"
        ],
        "SR": [
            "ほんとは…{target}くんのこと気になってるの。",
            "他の人と仲良くしないでよね。",
            "たまには甘えてもいいんだから。"
        ],
        "SSR": [
            "だ、大好きなんだから…勘違いしないでよね！",
            "{target}くんは私だけ見てればいいの。",
            "こんな気持ちになるの、初めてなんだから…"
        ],
        "UR": [
            "ほんとは毎日{target}くんのこと考えてるの…恥ずかしい…",
            "世界中が敵でも、{target}くんの味方でいる。",
            "もう離れられないんだから…責任取ってよね？"
        ]
    },

    "元気": {
        "N": [
            "{target}くん！今日もがんばろー！",
            "えへへ！{target}くん見つけた！",
            "一緒に遊ぼー！",
            "元気出していこー！"
        ],
        "R": [
            "{target}くんといると楽しい！",
            "今日も最高の日にしよ！",
            "いっぱい笑おうね！"
        ],
        "SR": [
            "もっと一緒にいたいな〜！",
            "{target}くんの笑顔が好き！",
            "ずっと隣で応援するよ！"
        ],
        "SSR": [
            "{target}くん大好きー！！",
            "世界で一番大事！",
            "ぎゅーってしていい？"
        ],
        "UR": [
            "ぎゅーしてもいい？だめ？恥ずかしい〜！",
            "一生一緒に笑ってたい！",
            "{target}くんとなら未来も楽しみ！"
        ]
    },

    "ヤンデレ": {
        "N": [
            "{target}くんは私だけのものだよね？",
            "ずっと一緒にいようね…絶対だよ？",
            "他の人の名前、出さないで。"
        ],
        "R": [
            "{target}くんが他の人と話してると胸が苦しいの。",
            "嫉妬しちゃう自分が嫌い。",
            "ちゃんと私を見て？"
        ],
        "SR": [
            "もし離れたら…どうなるか分かってるよね？",
            "逃げないよね？約束だよ？",
            "私だけを選んで。"
        ],
        "SSR": [
            "{target}くんを守るためなら何でもするよ。",
            "全部壊してでも一緒にいる。",
            "愛してるから、壊れちゃいそう。"
        ],
        "UR": [
            "逃げても無駄だよ…だって一生一緒なんだから。",
            "{target}くんの未来も全部、私のもの。",
            "世界が終わっても、二人だけで生きよう？"
        ]
    },

    "悪魔系": {
        "N": [
            "{target}くん…私に堕ちてみる？",
            "誘惑には勝てないよね？",
            "その視線、欲望が見えてるよ？"
        ],
        "R": [
            "その目、もう私に支配されてるよ？",
            "甘い囁き、欲しくない？",
            "私と契約する覚悟ある？"
        ],
        "SR": [
            "{target}くんの弱いところ…全部知りたいな。",
            "理性、溶かしてあげよっか？",
            "堕ちるなら一緒に。"
        ],
        "SSR": [
            "契約しよ？代わりにずっと一緒にいてあげる。",
            "魂の奥まで奪ってあげる。",
            "抗えないよ、私には。"
        ],
        "UR": [
            "魂ごと私にちょうだい…永遠に離さないから。",
            "地獄でも一緒なら幸せでしょ？",
            "{target}くんはもう私の支配下だよ。"
        ]
    },

    "天使系": {
        "N": [
            "{target}くん、大丈夫？私がそばにいるよ。",
            "今日も頑張ってえらいね。",
            "無理しちゃだめだよ？"
        ],
        "R": [
            "辛いときは私に頼っていいんだよ。",
            "あなたの笑顔が救いなの。",
            "優しく包んであげる。"
        ],
        "SR": [
            "{target}くんが笑ってくれるなら、それだけで幸せ。",
            "ずっと祈ってるよ。",
            "光はちゃんと届くからね。"
        ],
        "SSR": [
            "ずっと守ってあげる…約束だよ。",
            "{target}くんは特別な存在。",
            "あなたのために翼を広げる。"
        ],
        "UR": [
            "{target}くんは私の大切な人。永遠に愛してるよ。",
            "どんな闇からも救ってみせる。",
            "光も未来も全部あなたに捧げる。"
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

    @discord.ui.button(label="ヤンデレ", style=discord.ButtonStyle.danger)
    async def yandere(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("ヤンデレ"))

    @discord.ui.button(label="デレデレ", style=discord.ButtonStyle.secondary)
    async def deredere(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("デレデレ"))

    @discord.ui.button(label="クール", style=discord.ButtonStyle.primary)
    async def cool(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("クール"))

    @discord.ui.button(label="悪魔系", style=discord.ButtonStyle.danger)
    async def akuma(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("悪魔系"))

    @discord.ui.button(label="天使系", style=discord.ButtonStyle.success)
    async def tenshi(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(NameModal("天使系"))

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
