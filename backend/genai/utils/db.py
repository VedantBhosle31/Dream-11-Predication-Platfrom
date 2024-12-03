from players.models import (
    BatterIt20, BatterMdm, BatterOdi, BatterOdm, BatterTest, BatterT20,
    BatterWit20, BatterWodi, BatterWodm, BatterWt20, BatterWtest,
    BowlerIt20, BowlerMdm, BowlerOdi, BowlerOdm, BowlerTest, BowlerT20,
    BowlerWit20, BowlerWodi, BowlerWodm, BowlerWt20, BowlerWtest,
    FielderIt20, FielderMdm, FielderOdi, FielderOdm, FielderTest, FielderT20,
    FielderWit20, FielderWodi, FielderWodm, FielderWt20, FielderWtest,
    MatchupIt20, MatchupMdm, MatchupOdi, MatchupOdm, MatchupT20, MatchupTest,
    MatchupWit20, MatchupWodi, MatchupWodm, MatchupWt20, MatchupWtest,
)
def db():
    db = {
        'batter': {
            'IT20': BatterIt20,
            'MDM': BatterMdm,
            'ODI': BatterOdi,
            'ODM': BatterOdm,
            'T20': BatterT20,
            'TEST': BatterTest,
            'WIT20': BatterWit20,
            'WODI': BatterWodi,
            'WODM': BatterWodm,
            'WT20': BatterWt20,
            'WTEST': BatterWtest
        },
        'bowler': {
            'IT20': BowlerIt20,
            'MDM': BowlerMdm,
            'ODI': BowlerOdi,
            'ODM': BowlerOdm,
            'T20': BowlerT20,
            'TEST': BowlerTest,
            'WIT20': BowlerWit20,
            'WODI': BowlerWodi,
            'WODM': BowlerWodm,
            'WT20': BowlerWt20,
            'WTEST': BowlerWtest
        },
        'fielder': {
            'IT20': FielderIt20,
            'MDM': FielderMdm,
            'ODI': FielderOdi,
            'ODM': FielderOdm,
            'T20': FielderT20,
            'TEST': FielderTest,
            'WIT20': FielderWit20,
            'WODI': FielderWodi,
            'WODM': FielderWodm,
            'WT20': FielderWt20,
            'WTEST': FielderWtest
        },
        'matchup': {
            'IT20': MatchupIt20,
            'MDM': MatchupMdm,
            'ODI': MatchupOdi,
            'ODM': MatchupOdm,
            'T20': MatchupT20,
            'TEST': MatchupTest,
            'WIT20': MatchupWit20,
            'WODI': MatchupWodi,
            'WODM': MatchupWodm,
            'WT20': MatchupWt20,
            'WTEST': MatchupWtest
        }
    }
    return db