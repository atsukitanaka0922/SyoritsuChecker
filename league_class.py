from operator import itemgetter
from match_class import Match

class League:
    def __init__(self, name):
        """
        リーグ情報
        
        Args:
            name (str): リーグ名
        """
        self.name = name
        self.teams = {}  # チームID -> Teamオブジェクト
        self.matches = []  # 試合リスト
        self.current_round = 1
    
    def add_team(self, team):
        """
        リーグにチームを追加
        
        Args:
            team (Team): チームオブジェクト
        """
        self.teams[team.id] = team
    
    def get_team(self, team_id):
        """
        チームIDからチームを取得
        
        Args:
            team_id (str): チームID
            
        Returns:
            Team: チームオブジェクト、存在しない場合はNone
        """
        return self.teams.get(team_id)
    
    def get_team_by_name(self, team_name):
        """
        チーム名からチームを取得
        
        Args:
            team_name (str): チーム名
            
        Returns:
            Team: チームオブジェクト、存在しない場合はNone
        """
        for team in self.teams.values():
            if team.name == team_name:
                return team
        return None
    
    def create_match(self, home_team_id, away_team_id):
        """
        試合を作成
        
        Args:
            home_team_id (str): ホームチームID
            away_team_id (str): アウェイチームID
            
        Returns:
            Match: 作成された試合オブジェクト、チームが存在しない場合はNone
        """
        home_team = self.get_team(home_team_id)
        away_team = self.get_team(away_team_id)
        
        if not home_team or not away_team:
            return None
        
        match = Match(home_team, away_team, round_number=self.current_round)
        self.matches.append(match)
        return match
    
    def next_round(self):
        """
        次のラウンドに進む
        """
        self.current_round += 1
    
    def get_standings(self):
        """
        リーグ順位表を取得
        
        Returns:
            list: [(Team, 勝点, 勝率, 得失点差), ...] の形式でソート済み
        """
        standings = []
        for team in self.teams.values():
            standings.append((
                team,
                team.points(),
                team.win_rate(),
                team.goal_difference()
            ))
        
        # 勝点 > 勝率 > 得失点差 の順でソート
        return sorted(
            standings,
            key=itemgetter(1, 2, 3),
            reverse=True
        )
    
    def get_player_rankings(self):
        """
        選手の勝率ランキングを取得
        
        Returns:
            list: [(Player, 勝率, 試合数), ...] の形式でソート済み
        """
        all_players = []
        for team in self.teams.values():
            for player in team.players.values():
                all_players.append((
                    player,
                    player.win_rate(),
                    player.matches_played
                ))
        
        # 1試合以上出場している選手のみ、勝率降順でソート
        qualified_players = [p for p in all_players if p[2] > 0]
        return sorted(
            qualified_players,
            key=itemgetter(1, 2),
            reverse=True
        )
    
    def __str__(self):
        """
        リーグ情報の文字列表現
        """
        return f"{self.name} - {len(self.teams)}チーム, {len(self.matches)}試合, 現在Round {self.current_round}"