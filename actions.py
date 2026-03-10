import random

# ==========================================
# WS 核心斩杀 Action 映射表 (独立模块)
# ==========================================
# 所有的 Action 函数都严格接收三个参数：
# eng: GameEngine 实例 (你的游戏物理引擎，用于调用各种基础规则)
# src: Card 实例 (触发该效果的源卡牌)
# amt: int (效果相关的数值，如烧血量、推牌量)

ACTION_MAP = {
    # 1. 标准烧血 (可被取消)
    "Burn": lambda eng, src, amt: eng.deal_damage(amt),
    
    # 2. 武藏烧 (看顶等级+1)
    "Musashi": lambda eng, src, _: eng.deal_damage(eng.get_opp_top_level() + 1),
    
    # 3. 传火 (通常挂在 OnDamageCancel 触发器上)
    "PassTheTorch": lambda eng, src, amt: eng.deal_damage(amt),
    
    # 4. 推底烧 (推底 X 枚，根据 CX 数烧)
    "BottomMillBurn": lambda eng, src, amt: eng.deal_damage(eng.mill_opp(amt, from_top=False)),
    
    # 5. 傲慢加特林 (魂点拆分成 X 次 1 伤)
    "SplitAttack": lambda eng, src, _: [eng.deal_damage(1) for _ in range(getattr(src, 'soul', 1))],
    
    # 6. 强制进血 (无法被取消)
    "ForcedClockBurn": lambda eng, src, amt: eng.take_damage(amt),
    
    # 7. 判魂烧 (RaDragon: 判定有魂标则烧 X)
    "RaDragon": lambda eng, src, amt: eng.deal_damage(amt) if eng.check_player_top("soul") else None,
    
    # 8. 摩卡 (Moca: 封印牌顶 CX)
    "Moca": lambda eng, src, amt: eng.moca_effect(amt),
    
    # 9. 再动 (Restand)
    "Restand": lambda eng, src, _: eng.simulate_attack(src),
    
    # 10. 封顶 (打倒时将对手角色放回牌顶 - 模拟为下次攻击必中)
    "ReverseTopDeck": lambda eng, src, _: eng.opp_deck.insert(0, {"is_cx": False, "level": 0}),
    
    # 11. 踢人进血 (ClockKick)
    "ClockKick": lambda eng, src, _: eng.take_damage(1),
    
    # 12. 推顶烧 (推顶 X 枚，根据 CX 数烧)
    "OppTopMillBurn": lambda eng, src, amt: eng.deal_damage(eng.mill_opp(amt, from_top=True)),
    
    # 13. 查自顶烧 (自己顶是 L3 或魂标则烧 X)
    "PlayerTopCheckBurn": lambda eng, src, amt: eng.deal_damage(amt) if eng.check_player_top("level3") else None
}