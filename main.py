# 必要なクラスをインポート
from player_class import Player
from team_class import Team
from match_class import Match
from league_class import League
from ui_class import LeagueUI

def main():
    """
    メイン処理
    """
    try:
        # リーグの作成
        league_name = input("リーグ名を入力してください: ")
        league = League(league_name)
        
        # UIの作成
        ui = LeagueUI(league)
        
        # メインループ
        while True:
            command = ui.main_menu()
            
            if command == "1":
                ui.team_menu()
            elif command == "2":
                ui.player_menu()
            elif command == "3":
                ui.match_menu()
            elif command == "4":
                ui.stats_menu()
            elif command == "5":
                ui.file_menu()  # ファイル操作メニュー
            elif command == "0":
                # 終了前に保存確認
                if league.teams or league.matches:
                    save_confirm = input("大会データを保存しますか？ (y/n): ")
                    if save_confirm.lower() == 'y':
                        from league_storage import LeagueStorage
                        storage = LeagueStorage()
                        if storage.save_league(league):
                            print(f"大会「{league.name}」のデータを保存しました。")
                        else:
                            print("保存に失敗しました。")
                
                print("アプリケーションを終了します。")
                break
            else:
                input("無効なコマンドです。Enterキーを押してください...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        input("Enterキーを押して終了します...")

if __name__ == "__main__":
    main()