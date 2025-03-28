class Team:
    def __init__(self, id, name):
        """
        チーム情報
        
        Args:
            id (str): チームID
            name (str): チーム名
        """
        self.id = id
        self.name = name
        self.players = {}  # 選手ID -> Playerオブジェクト
        
        # チーム成績
        self.matches_played = 0  # 試合数
        self.wins = 0            # 勝利数
        self.losses = 0          # 敗北数
        self.draws = 0           # 引き分け数
        self.goals_for = 0       # 得点
        self.goals_against = 0   # 失点
    
    def add_player(self, player):
        """
        チームに選手を追加
        
        Args:
            player (Player): 追加する選手オブジェクト
        """
        player.team_id = self.id
        self.players[player.id] = player
    
    def add_match_result(self, own_score, opponent_score, result):
        """
        チームの試合結果を追加
        
        Args:
            own_score (int): 自チームの得点
            opponent_score (int): 相手チームの得点
            result (str): '○' (勝ち), '×' (負け), or '△' (引き分け)
        """
        self.matches_played += 1
        self.goals_for += own_score
        self.goals_against += opponent_score
        
        if result == '○':
            self.wins += 1
        elif result == '×':
            self.losses += 1
        elif result == '△':
            self.draws += 1
    
    def win_rate(self):
        """
        チームの勝率を計算
        
        Returns:
            float: 勝率 (0.0 ~ 1.0)、試合数が0の場合は0を返す
        """
        if self.matches_played == 0:
            return 0.0
        return self.wins / self.matches_played
    
    def points(self):
        """
        勝ち点を計算（勝=3点, 引分=1点, 負=0点）
        
        Returns:
            int: 勝ち点
        """
        return self.wins * 3 + self.draws * 1
    
    def goal_difference(self):
        """
        得失点差を計算
        
        Returns:
            int: 得失点差
        """
        return self.goals_for - self.goals_against
    
    def __str__(self):
        """
        チーム情報の文字列表現
        """
        basic = f"{self.name} ({len(self.players)}人)"
        stats = f"成績: {self.wins}勝 {self.losses}敗 {self.draws}引分 勝率: {self.win_rate():.3f}"
        points = f"勝点: {self.points()}点 得点: {self.goals_for} 失点: {self.goals_against} 得失点差: {self.goal_difference()}"
        return f"{basic}\n{stats}\n{points}"