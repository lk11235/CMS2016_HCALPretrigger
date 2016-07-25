import FWCore.ParameterSet.Config as cms

# make L1 ntuples from RAW+RECO

from Configuration.StandardSequences.Eras import eras
process = cms.Process("L1NTUPLE",eras.Run2_2016)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load("Configuration.StandardSequences.RawToDigi_Data_cff")
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('Configuration.StandardSequences.Eras')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.Reconstruction_Data_cff')

# global tag
process.GlobalTag.globaltag = '80X_dataRun2_HLT_v12'

process.p = cms.Path(
        process.RawToDigi
        )

process.schedule = cms.Schedule(process.p)

from L1Trigger.L1TNtuples.customiseL1Ntuple import L1NtupleRAW,L1NtupleTFileOut 
process = L1NtupleRAW(process)
process = L1NtupleTFileOut(process) 

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# Input source
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring() 
process.source = cms.Source ("PoolSource",
                             fileNames = readFiles,
                             secondaryFileNames = secFiles
                             )

readFiles.extend( [
    "file:/afs/cern.ch/user/l/lkang/eos/cms/store/data/Run2016B/JetHT/RAW/v1/000/272/762/00000/50F701BA-E213-E611-A459-02163E011DAA.root" 
    #"/store/data/Run2016B/JetHT/RAW/v1/000/272/760/00000/7A42AE55-D513-E611-9D36-02163E011976.root"
    ] )
