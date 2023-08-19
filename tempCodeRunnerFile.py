@tree.command(name="today", description="오늘 백준에서 푼 문제를 보여줍니다.", aliases = ["정산","hi"],guild=1110101899312631808)
async def today_command(interaction, baekjoon_id: str = None):
    # await interaction.response.send_message("Command is working!")
    if baekjoon_id == None:
        if interaction.user.id in user_data:
            baekjoon_id = user_data[interaction.user.id]
        else:
            await interaction.response.send_message("유저 id를 입력하세요!")
            return
    try:
        embed = today_baekjoon(baekjoon_id)  # Define this function
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print(e)
        await interaction.response.send_message("사용자를 찾을 수 없습니다.")