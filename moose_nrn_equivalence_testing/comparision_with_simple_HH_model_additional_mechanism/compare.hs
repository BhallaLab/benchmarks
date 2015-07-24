-- compre two csv file.

import System.Environment
import Text.CSV as TC
import Data.Map as DM
import Data.Binary as DB
import Data.Maybe
import Data.ByteString.Lazy.Char8 as DBC

-- This function converts bytestring to Float
convertToFloat :: DM.Map k [DBC.ByteString] -> DM.Map k [Float]
convertToFloat dataMap = DM.map (\row -> Prelude.map (\x -> DB.decode x::Float) row ) dataMap

zipWithTime dataMap =  DM.map (\x -> Prelude.zip timeVec x ) dataMap where 
    timeVec = DM.findWithDefault (TC.pack "time") [] dataMap

compareMooseAndNeuron mooseMap nrnMap = do
    let mooseSIMap = convertToFloat mooseMap
    -- Multiply each entry of neuron by 1e-3 to convert it to SI units.
    let nrnSIMap = DM.map(\row -> Prelude.map (\x -> 1e-3*x) row) $ convertToFloat nrnMap
    -- Zip these maps with time
    let mooseSIMapWithTime = zipWithTime mooseSIMap
    let nrnSIMapWithTime = zipWithTime nrnSIMap
    return 1

main = do
    files <- getArgs
    dataMaps <- mapM TC.parseCSV files
    difference <- compareMooseAndNeuron (dataMaps!!0) (dataMaps!!1)
    print $ difference
    putStrLn $ "Done"
    

