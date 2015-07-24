module Text.CSV (parseCSV) where 

import qualified Data.Map  as DM
import System.FilePath
import qualified Data.ByteString.Lazy.Char8 as DBC

getColumn index [] = []
getColumn index (r:rs) = r!!index : getColumn index rs

convertToMap [] _ _ dataM = dataM
convertToMap (h:hs) dlist colIndex dataM = convertToMap hs dlist (colIndex+1) (DM.insert h col dataM)
    where col = getColumn colIndex dlist

parseCSV :: FilePath -> IO (DM.Map DBC.ByteString [DBC.ByteString])
parseCSV filePath = do 
    bytes <- DBC.readFile filePath 
    let lines = map (\x -> DBC.split ',' x) $ DBC.split '\n' bytes
    let dataMap = convertToMap (head lines) (tail lines) 0 DM.empty
    return dataMap

test = do
    dataMap <- parseCSV "./moose_results.csv"
    print $ DM.lookup (DBC.pack "time") dataMap
    putStrLn $ "Done testing"
