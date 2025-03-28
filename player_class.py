class Player:
    def __init__(self, id, name, team_id=None, position=None, age=None):
        """
        選手のプロフィール情報
        
        Args:
            id (str): 選手ID
            name (str): 選手名
            team_id (str, optional): 所属チームID
            position (str, optional): ポジション
            age (int, optional): 年齢
        """
        self.id = id
        self.name = name
        self.team_id = team_id
        self.position = position
        self.age = age
        
        # 成績情報
        self.matches_played = 0  # 試合数
        self.wins = 0            # 勝利数
        self.losses = 0          # 敗北数
        self.draws = 0           # 引き分け数
    
    def add_result(self, result):
        """
        選手の試合結果を追加
        
        Args:
            result (str): '○' (勝ち), '×' (負け), or '△' (引き分け)
        """
        self.matches_played += 1
        if result == '○':
            self.wins += 1
        elif result == '×':
            self.losses += 1
        elif result == '△':
            self.draws += 1
    
    def win_rate(self):
        """
        勝率を計算
        
        Returns:
            float: 勝率 (0.0 ~ 1.0)、試合数が0の場合は0を返す
        """
        if self.matches_played == 0:
            return 0.0
        return self.wins / self.matches_played
    
    def __str__(self):
        """
        選手情報の文字列表現
        """
        profile = f"{self.name}"
        if self.position:
            profile += f" ({self.position})"
        if self.age:
            profile += f", {self.age}歳"
        
        stats = f"成績: {self.wins}勝 {self.losses}敗 {self.draws}引分 勝率: {self.win_rate():.3f}"
        return f"{profile}\n{stats}"