from models import batter_IT20, batter_MDM, batter_ODI, batter_ODM, batter_T20, batter_Test, batter_WIT20, batter_WODI, batter_WODM, batter_WT20, batter_WTest, bowler_IT20, bowler_MDM, bowler_ODI, bowler_ODM, bowler_T20, bowler_Test, bowler_WIT20, bowler_WODI, bowler_WODM, bowler_WT20, bowler_WTest, fielder_IT20, fielder_MDM, fielder_ODI, fielder_ODM, fielder_T20, fielder_Test, fielder_WIT20, fielder_WODI, fielder_WODM, fielder_WT20, fielder_WTest, matchup_IT20, matchup_MDM, matchup_ODI, matchup_ODM, matchup_T20, matchup_Test, matchup_WIT20, matchup_WODI, matchup_WODM, matchup_WT20, matchup_WTest

def db():
    db = {
        'batter': {
            'IT20': batter_IT20,
            'MDM': batter_MDM,
            'ODI': batter_ODI,
            'ODM': batter_ODM,
            'T20': batter_T20,
            'TEST': batter_Test,
            'WIT20': batter_WIT20,
            'WODI': batter_WODI,
            'WODM': batter_WODM,
            'WT20': batter_WT20,
            'WTEST': batter_WTest
        },
        'bowler': {
            'IT20': bowler_IT20,
            'MDM': bowler_MDM,
            'ODI': bowler_ODI,
            'ODM': bowler_ODM,
            'T20': bowler_T20,
            'TEST': bowler_Test,
            'WIT20': bowler_WIT20,
            'WODI': bowler_WODI,
            'WODM': bowler_WODM,
            'WT20': bowler_WT20,
            'WTEST': bowler_WTest
        },
        'fielder': {
            'IT20': fielder_IT20,
            'MDM': fielder_MDM,
            'ODI': fielder_ODI,
            'ODM': fielder_ODM,
            'T20': fielder_T20,
            'TEST': fielder_Test,
            'WIT20': fielder_WIT20,
            'WODI': fielder_WODI,
            'WODM': fielder_WODM,
            'WT20': fielder_WT20,
            'WTEST': fielder_WTest
        },
        'matchup': {
            'IT20': matchup_IT20,
            'MDM': matchup_MDM,
            'ODI': matchup_ODI,
            'ODM': matchup_ODM,
            'T20': matchup_T20,
            'TEST': matchup_Test,
            'WIT20': matchup_WIT20,
            'WODI': matchup_WODI,
            'WODM': matchup_WODM,
            'WT20': matchup_WT20,
            'WTEST': matchup_WTest
        }
    }
    return db