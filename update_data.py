from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json
import random
import threading
import time
import pandas as pd
import yfinance as yf

tickers_list = ["NOW","TDG","VEEV","CRM","LSS.PA","DUOL","NFLX","CRCT","PYPL","WKL.AS","DASTY","KNEBV.HE","ALPM.PA","FDS","EBAY","CPRT","WMT","NVDA","PTON","ASML","HSIC","IDXX","ADSK","V","NEM","TECN.SW","IFCN.SW","PHIA.AS"
                ,"EKTA-B.ST","NOVO-B.CO","TEL","PLX","KO","AAPL","GIVN.SW","NOK","ASSA-B.ST","MICC","SBUX","XOM","COST","NKE","TSLA","OERL.SW","CDNS","ADYEN.AS","AMS.MC","MCD","BA","ZAL.DE","SHOP","SGPYY","GAW.L","WK","MSCI","TEMN.SW",
                "PLNT","CSCO","VRSK","DE","DIM.PA","MTX.DE","MC.PA","SSNC","DASH","W","QCOM","BESI.AS","INPOY","DHR","HD","CAT","PG","DEO","UHR.SW","CFR.SW","MGDDY","OR.PA","SY1.DE","2UA.F","RMV.L","RR.L","ITRK.L","COLO-B.CO","BATS.L",
                "SMIN.L","ROR.L","SPX.L","AV.L","SN.L","AI.PA","DG.PA","RI.PA","SW.PA","CPG.L","EXPN.L","FICO","NEDAP.AS","EDEN.PA","ALC","SMNNY","SHW","JNJ","CRWD","ABNB","FTNT","TEAM","TRI","ISRG","PLTR","CMCSA","ORLY","ARM","LR.PA",
                "GEBN.SW","KNIN.SW","HOLN.SW","LONN.SW","SIEGY","WRT1V.HE","KCR.HE","STERV.HE","BVI.PA","RMS.PA","BN.PA","SU.PA","SPOT","HNNMY","INTU","GWRE","MNST","FAST","ERNXY","FUR.AS","AMG.AS","VPK.AS","ISS.CO","DEMANT.CO",
                "MAERSK-B.CO","LTMC.MI","REL.L","HWDN.L","ANET","APH","MANH","IMI1.F","AFG.OL","MCO","FTNT","ECL","EQIX","KLAC","COUR","ISRG","AMT","LOTB.BR","BFIT.AS","CRBN.AS","AMP.MI","G1A.DE","DRW3.F","RHM.DE","UNH","TRIP","GIS",
                "SIKA.SW","FISV","SAUHY","UHR.SW","BNTGY","TMRAY","CAP.PA","POOL","EVO.ST","ATCO-A.ST","SDVKY","HEXA-B.ST","SAAB-B.ST","ESSITY-B.ST","MCK","GDDY","WIX","CL","ADP","FTV","TTEK","WRLD","ITW","MTD","SGO.PA","ERF.PA",
                "STZ","DG","SIRI","CROX","MNDY","CALY","HOG","AMGN","GS","IBM","RIO","GSK","NG","LLOY.L","NWG","KLAC","APP","WDC","BKR","ALNY","TTWO","AVGO","AXON","CTAS","LRCX","ADI","AMD","BKNG","AEP","ADBE","ADP","GILD","HON",
                "CSGP","INSM","VZ","SHW","AXP","AMZN","DIS","CVX","JPM","TRV","MRK","MMM","CON.DE","ADDYY","BEI.DE","EONGY","ALV.DE","RAND.AS","MT","IMCD.AS","AEG","AKZA.AS","INGA.AS","NN.AS","KPN.AS","AD.AS","AALB.AS","ABN.AS","ASRNL.AS",
                "HEIA.AS","LKFT.AS","ULVR.L","URW.PA","BNP.PA","KER.PA","ORA.PA","TEP.PA","VIE.PA","STM","CA.PA","RNO.PA","PUB.PA","GLE.PA","CTAS","CHTR","CTSH","DDOG","GEHC","KHC","WDAY","XEL","MU","MELI","MDLZ","ODFL","PANW","PCAR",
                "MPWR","BAS.DE","TXN","ZS","NXPI","SMMNY","BMW.DE","G24.DE","SAP","DB1.DE","DHLGY","BAYRY","RWE.DE","FME.DE","VNA.DE","FRE.DE","HEN3.DE","PAH3.DE","SIE.DE","AIR.DE","DTE.DE","VOW3.DE","MRK","MUV2.DE","MBG.DE","CARL-B.CO",
                "NKT.CO","VWS.CO","NOVO-B.CO","PNDORA.CO","RBREW.CO","AMBU-B.CO","ORSTED.CO","BVNRY","FLS","GN.CO","ROCK-B.CO","JYSK.CO","GMAB","DSV.CO","DANSKE.CO","TM2.F","TRYG.CO","ZEAL.CO","HO.PA","ACA.PA","BOUYY","SAFRY","CS.PA",
                "STLA","BNP.PA","TTE","AIR.PA","SAN.PA","ENGI.PA","AC.PA","VIA.PA","EL.PA","INTC","MCHP","MRVL","MSFT","STX","ROST","TMUS","PDD","PAYX","CEG","CSX","CCEP","FANG","FER","ROP","REGN","PEP","LIN","KDP","HNR1.DE","QIA.F",
                "HEI","CBK","DTG","SNPS","TXN","VRTX","DXCM","EXC","MAR","META","MSTR","GOOGL","KNIN.SW","LOGI","SREN.SW","SIKA.SW","SOON.SW","SCMN.SW","SMWH.L","AMAT","UBS","NESN.SW","NOVN.SW","ROP.SW","SLHN.SW","ZURN.SW","ABBN.SW",
                "SKF-B.ST","ALFA.ST","EQT","EPI-A.ST","ADDT-B.ST","BOL.ST","ERIC-B.ST","TELIA.ST","SKA-B.ST","TEL2-B.ST","TSCO.L","WEIR.L","RTO","CRDA.L","BRBY.L","HLMA.L","GLEN.L","BNZL.L","PSON.L","SGRO.L","SCA-B.ST","AZN","SAND.ST",
                "VOLCAR-B.ST","BAB.L","BA.L","BP","ANTO.L","SBRY.L","SHEL","KGF.L","HLN","FRES.L","INF.L","JD","HSX.L","MNDI.L","WTB.L","VOD","STAN.L","MKS.L","RKT.L","RACE","DPLM.L","CNA.L","BT-A.L","DCC.L","ENT.L","PSON.L","PSN",
                "ITX.MC","AENA.MC","GRF.MC","IDR.MC","MAP.MC","CLNX.MC","REP.MC","LOG.MC","FDR.MC","SLR.MC","MRO.L","SVT.L","CTEC.L","ABF.L","IAG.L","IMB.L","NXT.L","STAN.L","SDLF.L","SSE.L","UU.L","BBOX.L","STJ.L","AAL.L","ADM.L",
                "AAF.L","BARC.L","BLND.L","CCH.L","BKG.L","LGEN.L","SLB","SNA","VLTO","APD","BBY","GEN","GRMN","GD","IBKR","WM","VMC","WST","SYY","TPR","SJM","SWK","RL","RVTY","RSG","ALLE","ALGN","AFL","AZO","AVY","ANET","APTV","BALL",
                "AKAM","ALB","ACN","BLDR","BG","BF-B","UBER","TJX","TSN","TRMB","TT","TYL","TSCO","TGT","ULTA","SWKS","STE","SW","STLD","LUV","STT","TER","TXT","TMO","UNP","URI","WAT","WAB","GWW","SOLV","PM","PPG","RMD","RTX","DGX",
                "ROL","PWR","PHM","VRSN","VTRS","YUM","ZBH","ZBRA","WYNN","ZTS","XYL","WSM","WMB","TKO","TTD","TDY","TRGP","SMCI","SYK","NDAQ","NUE","NVR","NTAP","SPG.F","NDSN","ZTF.L","ANA.MC","ACX.MC","PUIG.MC","ELE.MC","NTGY.MC",
                "ROVI.MC","NCLH","NOC","NWSA","MOS","MSI","TAP","MOH","OMC","OKE","ORLY","OTIS","NRG","PH","NSC","ON","ORCL","PAYC","PKG","PPL","RCL","SPGI","UPS","UAL","WTW","TEL","TROW","ROK","Q","PNR","NTRS","NEM","LULU","LOW",
                "LMT","MTCH","MDT","MGM","MKC","MAS","MRSH","MLM","LYB","MA","AOS","ABT","MO","A","AMCR","ADM","AME","BR","BSX","WIE.VI","VOE.VI","ADRZY","ATS.VI","LNZ.VI","BG.VI","PAL.VI","DIE.DE","MELE.BR","SOLB.BR","UMI.BR",
                "ACKB.BR","FFARM.AS","LIGHT.AS","MICC","ACOMO.AS","NEDAP.AS","TFF.PA","PL8.F","SIGCY","BUCN.SW","SUN.SW","IP.MI","BZU.MI","NEXPF","PRY.MI","GET.PA","TYRES.HE","LXS.DE","DIA.MI","SESG.PA","FUTR.L","WOSG.L","RUI.PA",
                "HUH1V.HE","KGX.DE","AZE.BR","LISN.SW","YOU.L","EVS.BR","ITP.PA","INRN.SW","NOEJ.DE","KTN.F","FIE.F","FPE3.DE","JUN3.DE","NLM.F","BC8.F","KENDR.AS","VID.MC","LHA.DE","MONC.MI","DUFRY","TUB.BR","GALD.SW","DHER.DE",
                "BMXMF","BARN.SW","SALRY","PNDORA.CO","CPR.MI","HAG.DE","HOT.DE","INDT.ST","HOLM-B.ST","PRX.AS","SECU-B.ST","TREL-B.ST","UCB","ACSAF","ASM.AS","BEAN.SW","MGDDY","EVD.DE","EQNR","EVK.DE","LDO.MI","KGSPY","KBX.F","KBGGY",
                "ORKLY","SGSN.SW","UMG.AS","UPM.HE","VACN.SW","YARIY","SCHP.SW","SRT4.F","RYAAY","TEN.MI","VSURE.ST","WISE.L","WRT1V.HE","TIT.MI","TEF.MC","ERIC-B.ST","SUBCY","RXL.PA","SAGA-B.ST","PINE","RED.MC","NEM","NBIS","NESTE.HE",
                "NHYDY","KYGA.L","KESKOB.HE","JRONY","ENX.PA","FER","AKRBF","AER","AIBG.L","AGS.BR","HSBA.L","HBAN.SW","ENEL.MI","DSFIR.AS","EBO.DE","AYV.PA","BAMI.MI","BMED.MI","BMPS.MI","ALO.PA","ABI.BR","AMUN.PA","BZU.MI","DBK.DE",
                "METSO.HE","NIBE-B.ST","NDA-FI.HE","ORNBV.HE","OMV.VI","PST.MI","PRU","RAA.F","RBI.VI","REC.MI","SAMPO.HE","SDZ.SW","SHB-A.ST","ADP.PA","AGS.BR","ARGX","BTRW.L","BKT.MC","SAN","BBVA.MC","SAB.MC","BEIJ-B.ST","BCVN.SW",
                "BKW.SW","BCP.LS","BIRG.IR","CABK.MC","BPE.MI","BOL.ST","AM","FGR.PA","ELISA.HE","EDP.LS","EMSN.SW","EDV.L","ELI.BR","DNBBY","EDPR.LS","ENI.MI","FBK","EXO.AS","BALD-B.ST","GALP.LS","FORTUM.HE","G","GECFF","XGJ.F",
                "GBLB.BR","GET.PA","IBE.MC","IPSEY","IG.MI","INDU-C.ST","SEB-A.ST","SRG.MI","SGSN.SW","SOF.BR","SWED-A.ST","SDLF.L","TLX.F","SREN.SW","SYENS.BR","UU.L","UNI.MI","UCG.MI","TRN","SPSN.SW","SOBI.ST","LIFCO-B.ST","LUND-B.ST",
                "LAND","LEG.F","MNG.L","ISP.MI","LATO-B.ST","INVE-B.ST","BAER.SW","KBC.BR","LI.PA","CVC.AS","COV.PA","III.L","III.L","LSEG.L","PEGA","CIEN","CVNA","CI","CMG","DECK","DVA","EL","GEV","JBL","SNDK","HOOD","SPG","SYF","PFE",
                "PCG","PFG","PNW","PSX","CB","CHD","SCHW","CINF","CL","CRL","CF","CMS","CFG","CMI","ED","COP","COO","CME","CLX","CCI","CRH","DLR","DLTR","WEC","IT","FE","HRL","HWM","PODD","HUBB","HST","BEN","GPN","ABX","CHRW","CNP","BRO",
                "CARR","BXP","CBRE","ACGL","AIZ","ABBV","LNT","AES","ARE","ALL","ASHM.L","BAX","ATO","BNY","XYZ","BIIB","CBOE","COR","CNC","CDW","CPB","CVS","CTVA","DVN","GLW","CPAY","DRI","DOW","ETN","EW","EPAM","DUK","ETR","EMR","EME",
                "ELV","HAS","GNRC","HAL","GPC","HCA","HIG","GM","FCX","FSLR","BDX","BMY","ADP","TECH","MET","MRNA","LYV","MTB","MS","KEYS","IR","JCI","IFF","IP","IVZ","JKHY","JBHT","J","IQV","KLAC","COF","CPT","DHI","DD","D","DAL","DELL",
                "C","CAH","CCL","BLK","ERIE","EFX","EOG","EQT","FDS","EG","FDX","LEN","KMB","EXPD","EXE","EXPE","FFIV","F","FIS","FOX","AJG","AON","FIX","CAG","EIX","ESS","EVRG","ES","EXR","FRT","IRM","INVH","INCY","KEY","TPL","LII","LW",
                "KR","KMI","LHX","UDR","NEE","NI","PLD","O","RJF","PNC","PSA","PEG","PGR","PRU","BX","BAC","BRK-B","APA","APO","ARES","AMP","AWK","AEE","A","FITB","FRT","HLT","HUM","IEX","HSY","HPE","HPQ","LVS","LDOS","KIM","KKR","LLY",
                "MPC","DVN","P","HBAN","HII","ICE","L","OXY","T","COIN","DTE","WFC","WELL","VICI","WRB","VST","DOC","MAA","RF","REG","SBAC","SO","VTR","VLO","UHS","SRE","TFC","GE","CASY","COHR","ECHO","LITE","SLB","GE","VRT","QSR","BN",
                "HHH","SEG","HTZ","ADT","AAP","AAL","KMX","M","VNO","VFC","SIG","BWA","ZION","BFH","FOSL","GAP","AA","CNX","VAL","UNM","URBN","GF8.F","SPCX","NDA-FI.HE","SWDBY","SEBA.F","LIFCO-B.ST","INVE-B.ST","NIBE-B.ST","INDU-C.ST",
                "IBE.MC","UNI.MI","ACS.MC","SCYR.MC","RED.MC","ANE.MC","ENG.MC","COL.MC","ICAGY","MRL.MC","BGEO.L","LMP.L","MNG.L","PSH.L","LAND.L","X4Z.F","PCT.L","SMT.L","EDV.L","IGG.L","FERG","FCIT.L","IHG","III.L","ALW.L","LSEG.L",
                "LIN","ABI.BR","ACKB.BR","SOLB.BR","LOTB.BR","SYENS.BR","UMI.BR","ELI.BR","AED.BR","APAM","MONT.BR","AZE.BR","AGS.BR","WPHB.HM","MELE.BR","ARGX","KESKOB.HE","MANTA.HE","HUH1V.HE","KEMIRA.HE","TYRES.HE","BESI.AS","UMG.AS",
                "OUT1V.HE","VALMT.HE","KCR.HE","TIETO.HE","SSAB-B.ST","QTCOM.HE","GBLB.BR","IBS.LS","ACJ.F","NVG.LS","PHR.LS","COR.LS","CTT.LS","ZEHN.SW","JEN.DE","EGL.LS","SON.LS","NBA.LS","RENE.LS","NOS.LS","FLO.L","NORB-B.ST","MTLS",
                "VAN.BR","FLOB.BR","IBAB.BR","KIN.BR","TESB.BR","SIP.BR","ENRGY.BR","REC.BR","BAR.BR","BPOST.BR","ECONB.BR","IMMO.BR","ONWD.BR","ROU.BR","ONTEX.BR","HARB-B.CO","TCM.CO","HUSCO.CO","BIOPOR.CO","AGF-B.CO","GABR.CO",
                "TGAMES.CO","GREENM.CO","DONKEY.CO","BIF.CO","PFINV.CO","HVID.CO","RBLN-B.CO","RIAS-B.CO","IMPERO.CO","KONSOL.CO","DATA.CO","HOVE.CO","GJ.CO","KLEE-B.CO","STRINV.CO","FED.CO","AGAT.CO","CEMAT.CO","SIG.CO","FFARMS.CO",
                "RTX.CO","GYLD-A.CO","NNIT.CO","CBRAIN.CO","BO.CO","COLUM.CO","FLUG-B.CO","NORTHM.CO","HH.CO","SOLAR-B.CO","TRIFOR.CO","AOJ-B.CO","MTHH.CO","PARKEN.CO","TIV.CO","MATAS.CO"," NXFIL.AS"," AJAX.AS"," AVTX.AS","HYDRA.AS",
                "KENDR.AS","ALFEN.AS","MTRK.AS","AZRN.AS","DKUPL.PA","EXE.PA","ALNSE.PA","BLC.PA","LAT.PA","LOCAL.PA","5UP.F","ATEME.PA","ALHEX.PA","ALESE.PA","GET.DU","MDM.PA","ALMDT.PA","RBO.PA","ALLAN.PA","SFPI.PA","AKW.PA","PARP.PA",
                "ALLIX.PA","ALEXA.PA","ALCIS.PA","ALVU.PA","DEEZR.PA","ALSTW.PA","ALDLT.PA","ALRIB.PA","MLCMB.PA","ALCPB.PA","ALSTI.PA","BON.PA","GPE.PA","FSDV.PA","INF.PA","LIN.PA","PARRO.PA","MBWS.PA","ALBFR.PA","EFG.PA","TFF.PA",
                "ARAMI.PA","LNA.PA","PERR.PA","ALPG.PA","GAM.PA","CVX.PA","ALGIL.PA","KOF.PA","SMCP.PA","LPE.PA","ELIOR.PA","BEN.PA","JCQ.PA","ATO.PA","MALT.PA","SAMS.PA","NRG.PA","FCMC.PA","EQS.PA","QDT.PA","FGA.PA","SCHP.PA","SBT.PA",
                "CEN.PA","LBIRD.PA","ALSEM.PA","ASY.PA","AL2SI.PA","THEP.PA","AUB.PA","SDG.PA","BUR.PA","EXPL.PA","GLO.PA","UBI.PA","WAVE.PA","SAVE.PA","ALVDM.PA","MTU.PA","XFAB.PA","VAC.PA","CDA.PA","NRO.PA","GDS.PA","FNAC.PA","MRN.PA",
                "HAG.DE","ERA.PA","CLARI.PA","TFI.PA","DBG.PA","IPS.PA","VIV.PA","MMT.PA","PLNW.PA","ALHG.PA","EMEIS.PA","RBT.PA","STF.PA","NK.PA","ETL.PA","OPM.PA","FRVIA.PA","ESY.HM","SB1.DE","MSGL.HM","TC1.DE","SYT.DE","TIW.F",
                "SJJ.DE","HAW.DE","MZX.DE","ED4.DE","EVAC.DE","WOLF.DE","MUB.DE","SKB.DE","HMU.DE","FAA.DE","M7U.DE","AEIN.DE","LIK.DE","TTK.DE","TTR1.DE","AAG.DE","VRV.DE","GMM.DE","WEW.DE","BKHT.DE","B5A0.HM","EIS.F","LNSX.F",
                "BYW6.DE","BYW6.DE","ST5.DE","MED.DE","HNR1.DE","SBS.DE","ILM1.DE","ZIL2.DE","A1OS.DE","HOT.DE","ADN1.DE","F3C.DE","UZU.DE","BVB.DE","EKT.DE","A1OS.DE","HFG.DE","BIJ.DE","STM.DE","M12.DE","NOEJ.DE","LPK.DE","WSU.DE",
                "IVU.DE","SIN.DE","HDD.DE","IXX.DE","IFA1.DE","SGL.DE","NB2.DE","MUM.DE","PNE3.DE","EVT.DE","BSL.DE","PSM.DE","TPE.DE","PSAN.DE","PHH2.DE","NLM.DE","GFT.DE","D6H.DE","SSH.F","COK.DE","SHF.DE","MUB.DE","VINC.DE","TIMA.DE",
                "ASTA.VI","1INN.DE","CWC.DE","EUZ.DE","EUK3.DE","DOU.DE","MBB.DE","NA9.DE","NA9.DE","VOS.DE","TMV.DE","JST.DE","SFQ.DE","CHG.DE","GXI.DE","RHK.DE","LXS.DE","INH.DE","DUE.DE","ADV.DE","PFSE.DE","2GB.DE","NCH2.DE","AOF.DE",
                "KTN.DE","KCO.DE","SMHN.DE","HBH.DE","WAC.DE","PFV.DE","ACT.DE","HHFA.DE","YSN.DE","COP.DE","TNIE.DE","KSB3.DE","RDC.DE","HBM.DE","DEZ.DE","SAX.DE","DRW8.DE","CEC.DE","GBF.DE","S92.DE","SZU.DE","JEN.DE","KWS.DE","AFX.DE",
                "FNTN.DE","SDF.DE","ELG.DE","BOSS.DE","WAF.DE","SHA0.DE","FRA.DE","ZAL.DE","FPE3.DE","TKMS.DE","KGX.DE","EVD.DE","G24.DE","UTDI.DE","WCH.DE","IOS.DE","BC8.DE","1U1.DE","AIXA.DE","SPG.DE","AG1.DE","1SXP.DE","R3NK.DE",
                "OHB.DE","AMV0.DE","TUI1.DE","OBCK.DE","PUM.DE","KRN.DE","FIE.DE","SIX2.DE","SZG.DE","APTD.L","BKS.L","HSW.L","LIKE.L","MACF.L","PHAR.L","CGS.L","SHI.L","MOTR.L","SFR.L","TRI.L","XAR.L","FDM.L","IES.L","QTX.L","HPOW.L",
                "ACSO.L","EKF.L","AURR.L","RWA.L","SPEC.L","MPAC.L","VID.L","GTLY.L","DOTD.L","PRE.L","W7L.L","BRCK.L","CRST.L","AOM.L","RCH.L","EYE.L","SAA.L","AXS.L","CAM.L","KGH.L","TUNE.L","MCG.L","ECEL.L","SUP.L","CCP.L","GLE.L",
                "SAV.L","SYNT.L","MUL.L","SML.L","KMR.L","SNWS.L","BTG.L","FNTL.L","SRB.L","SRAD.L","MIDW.L","BOOT.L","VP..L","KP2.L","TSTL.L","ABDP.L","ELCO.L","CER.L","SRT.L","NET.L","FDEV.L","FSJ.L","ZTF.L","TRB.L","CNC.L","LTHM.L",
                "KEYS.L","SAG.L","ASY.L","JDG.L","NCC.L","ADVT.L","DIA.L","ELIX.L","OTB.L","WIL.L","VIC.L","MSI.L","VTU.L","HSP.L","BIG.L","EEE.L","AVG.L","CARD.L","CAML.L","FUTR.L","SWC.L","GMET.L","ALTN.L","CPI.L","NXR.L","KIST.L",
                "OPT.L","NIOX.L","SFOR.L","FRAN.L","AGY.L","TFW.L","FRP.L","WVIA.L","MARS.L","THG.L","DATA.L","PRV.L","BOWL.L","RST.L","MEGP.L","LSC.L","WIX.L","MSLH.L","AT..L","ALFA.L","YNGN.L","YNGA.L","MTL.L","AO.L","JSG.L","RWS.L",
                "JHD.L","GFM.L","TBTG.L","PINE.L","BMY.L","ATG.L","AVON.L","FTC.L","CHRT.L","ASC.L","SMWH.L","TUNG.L","HFD.L","PPH.L","BAG.L","AMS.L","IQE.L","EVPL.L","HFG.L","ITM.L","GFRD.L","PAGE.L","APN.L","COST.L","TRN.L","DOCS.L",
                "CVSG.L","VTY.L","AEP.L","RNWH.L","MGAM.L","GEN.L","PRN.L","DOM.L","VCT.L","DSCV.L","MOON.L","TRST.L","CWR.L","JDW.L","SPI.L","GAMA.L","FGP.L","PETS.L","FEVR.L","MONY.L","JUP.L","BREE.L","MPE.L","ZIG.L","BYIT.L","ELM.L",
                "GDWN.L","HAS.L","QQ.L","TATE.L","SRP.L","BWY.L","KLR.L","HTWS.L","ONT.L","CAN.L","OCDO.L","MGNS.L","GRG.L","GNC.L","GFTU.L","MAB.L","PFD.L","OXIG.L","ATYM.L","WOSG.L","DNLM.L","CURY.L","COA.L","BOY.L","CKN.L","CHG.L",
                "RHIM.L","SRC.L","CRN.L","SSPG.L","KNOS.L","RPI.L","KIE.L","FAN.L","TPK.L","FOUR.L","SNR.L","VLX.L","VSVS.L","REG1V.HE","ENENTO.HE","LINDEX.HE","KREATE.HE","VIK1V.HE","AUROORA.HE","REMEDY.HE","ANORA.HE","FSECURE.HE",
                "LASTIK.HE","ICP1V.HE","RELAIS.HE","PIHLIS.HE","ASPO.HE","CANATU.HE","KOSKI.HE","ETTE.HE","GOFORE.HE","REAKTOR.HE","SRV1V.HE","VERK.HE","SAVOX.HE","NOHO.HE","ORIOLA.HE","SFOODS.HE","HKFOODS.HE","TEM1V.HE","KSL.HE",
                "DIGIA.HE","ADMCM.HE","EXEL.HE","SSH1V.HE","SUY1V.HE","DETEC.HE","IQMX.HE","KALMAR.HE","VAIAS.HE","TYRES.HE","TIETO.HE","SANOMA.HE","PUUILO.HE","BITTI.HE","GRK.HE","ALMA.HE","YIT.HE","FSKRS.HE","TTALO.HE","FIA1S.HE",
                "SCANFL.HE","QTCOM.HE","HARVIA.HE","OLVAS.HE","PON1V.HE","KEMPOWR.HE","FRAMERY.HE","MUSTI.HE","ATRAV.HE","TOKMAN.HE","MEKKO.HE","PAMPALO.HE","RAIVV.HE","CASH.MC","CBAV.MC","TSK.MC","ENC.MC","EBROM.MC","EDR.MC","OHLA.MC",
                "GSJ.MC","MCM.MC","NXT.MC","AMP.MC","ALC.MC","DOM.MC","CLR.MC","TUB.MC","PRS.MC","TLGO.MC","IZER.MC","SOL.MC","AZK.MC","NAT.MC","SEC.MC","PRM.MC","ATRY.MC","SQRL.MC","ATSI.MC","IBG.MC","OLE.MC","NTH.MC","AI.MC","GAM.MC",
                "NEA.MC","VYT.MC","MDF.MC","AMEN.MC","VOC.MC","PUIG.MC","FCC.MC","ACX.MC","FDR.MC","SCYR.MC","CIRSA.MC","CIE.MC","EBRO.MC","DIA.MC","ENO.MC","CAF.MC","CMO.MC","VIS.MC","MEL.MC","ART.MC","DIGIS.MC","HBX.MC","GEST.MC",
                "IMC.MC","HOME.MC","PSG.MC","A3M.MC","VOW.OL","HKY.OL","KLDVK.OL","HDLY.OL","OTOVO.OL","WEST.OL","STECH.OL","SCANA.OL","BOR.OL","KING.OL","GENT.OL","INIFY.OL","STST.OL","ENSU.OL","LOKO.OL","GOD.OL","ITERA.OL","ININ.OL",
                "STRO.OL","IDEX.OL","CONTX.OL","ELABS.OL","HAV.OL","AKOBO.OL","ARR.OL","5PG.OL","WSTEP.OL","CAPSL.OL","CYVIZ.OL","BCS.OL","MVW.OL","EQVA.OL","PROXI.OL","LIFE.OL","CAVEN.OL","NTG.OL","HPUR.OL","NOM.OL","DSRT.OL","OCEAN.OL","2020.OL","TECH.OL","OBSRV.OL"

]

# Remove duplicates (many tickers appear several times) while keeping order
tickers_list = list(dict.fromkeys(tickers_list))

# --- Rate-limit settings ---------------------------------------------------
MAX_WORKERS = 3            # few parallel workers
MIN_REQUEST_INTERVAL = 0.6 # min seconds between ANY two Yahoo requests (global)
MAX_RETRIES = 5            # retries per request when rate limited
BACKOFF_BASE = 30          # seconds; doubles each retry (30, 60, 120, ...)
PASS_COOLDOWN = 300        # seconds to wait before re-trying failed tickers
MAX_PASSES = 3             # full passes over tickers that failed


class RateLimitExhausted(Exception):
    pass


_lock = threading.Lock()
_next_slot = 0.0  # earliest time the next request may be sent


def _is_rate_limit(exc):
    name = type(exc).__name__
    msg = str(exc).lower()
    return (
        "ratelimit" in name.lower()
        or "too many requests" in msg
        or "429" in msg
        or "rate limit" in msg
    )


def call_with_retry(fn):
    """Run a yfinance call through a global throttle; back off on rate limits."""
    global _next_slot
    for attempt in range(MAX_RETRIES + 1):
        # Global throttle (also used as a shared cooldown for all threads)
        with _lock:
            now = time.monotonic()
            wait = max(0.0, _next_slot - now)
            _next_slot = max(now, _next_slot) + MIN_REQUEST_INTERVAL + random.uniform(0, 0.3)
        if wait:
            time.sleep(wait)
        try:
            return fn()
        except Exception as e:
            if not _is_rate_limit(e):
                raise
            if attempt == MAX_RETRIES:
                raise RateLimitExhausted(str(e))
            delay = BACKOFF_BASE * (2 ** attempt) + random.uniform(0, 5)
            print(f"Rate limited, pausing all workers for {delay:.0f}s...")
            with _lock:  # make every thread wait out the cooldown
                _next_slot = max(_next_slot, time.monotonic() + delay)


def subtract_months(dt, months):
    year = dt.year - (months // 12)
    month = dt.month - (months % 12)
    if month <= 0:
        month += 12
        year -= 1
    days_in_month = [
        31,
        29
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        else 28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    day = min(dt.day, days_in_month[month - 1])
    return dt.replace(year=year, month=month, day=day)


# Calculate historical milestone dates relative to today
today = datetime.utcnow()
date_1m = subtract_months(today, 1)
date_6m = subtract_months(today, 6)
date_12m = subtract_months(today, 12)
date_36m = subtract_months(today, 36)


def fetch_ticker_data(ticker_symbol):
    print(f"Processing {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)

    # 1. Fetch info dictionary
    try:
        info = call_with_retry(lambda: ticker.info)
    except RateLimitExhausted:
        raise
    except Exception as e:
        print(f"Could not fetch info for {ticker_symbol}: {e}")
        info = {}

    trailing_pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    enterprise_value = info.get("enterpriseValue")
    dividend_yield = info.get("dividendYield")
    total_cash_fallback = info.get("totalCash")

    # New Datapoints from info
    fifty_two_week_high = info.get("fiftyTwoWeekHigh")
    fifty_two_week_low = info.get("fiftyTwoWeekLow")
    price_to_book = info.get("priceToBook")
    total_debt = info.get("totalDebt")
    total_revenue = info.get("totalRevenue")
    operating_margins = info.get("operatingMargins")
    profit_margins = info.get("profitMargins")
    return_on_assets = info.get("returnOnAssets")
    return_on_equity = info.get("returnOnEquity")
    website = info.get("website", "N/A")

    # Free Cash Flow (Current TTM)
    free_cash_flow = info.get("freeCashflow")
    if free_cash_flow is None:
        try:
            cf = call_with_retry(lambda: ticker.cash_flow)
            if not cf.empty and "Free Cash Flow" in cf.index:
                free_cash_flow = float(cf.loc["Free Cash Flow"].iloc[0])
            elif (
                not cf.empty
                and "Operating Cash Flow" in cf.index
                and "Capital Expenditure" in cf.index
            ):
                ocf = cf.loc["Operating Cash Flow"].iloc[0]
                capex = cf.loc["Capital Expenditure"].iloc[0]
                free_cash_flow = float(ocf + capex)
        except RateLimitExhausted:
            raise
        except Exception:
            pass

    # 2. Get Balance Sheet metrics
    cash_equivalents = "N/A"
    short_term_investments = "N/A"
    total_liabilities = "N/A"

    try:
        bs = call_with_retry(lambda: ticker.balance_sheet)
        if not bs.empty:
            for label in [
                "Cash And Cash Equivalents",
                "Cash Cash Equivalents And Short Term Investments",
            ]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (
                        isinstance(val, float) and str(val) == "nan"
                    ):
                        cash_equivalents = float(val)
                        break
            if cash_equivalents == "N/A" and total_cash_fallback is not None:
                cash_equivalents = float(total_cash_fallback)

            for label in ["Other Short Term Investments", "Short Term Investments"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (
                        isinstance(val, float) and str(val) == "nan"
                    ):
                        short_term_investments = float(val)
                        break

            for label in [
                "Total Liabilities Net Minority Interest",
                "Total Liabilities",
            ]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (
                        isinstance(val, float) and str(val) == "nan"
                    ):
                        total_liabilities = float(val)
                        break
    except RateLimitExhausted:
        raise
    except Exception as e:
        print(f"Could not fetch balance sheet for {ticker_symbol}: {e}")

    # 3. Historical Prices using auto_adjust=True (the 'Close' column is already adjusted)
    last_adj_close = "N/A"
    adj_close_1m = "N/A"
    adj_close_6m = "N/A"
    adj_close_12m = "N/A"
    adj_close_36m = "N/A"

    try:
        hist = call_with_retry(lambda: ticker.history(period="4y", auto_adjust=True))
        if not hist.empty and "Close" in hist.columns:
            last_adj_close = float(hist["Close"].iloc[-1])

            def get_price_at_date(target_dt):
                target_ts = pd.Timestamp(target_dt)
                if hist.index.tz is not None and target_ts.tz is None:
                    target_ts = target_ts.tz_localize(hist.index.tz)
                sub_hist = hist[hist.index <= target_ts]
                if not sub_hist.empty:
                    return float(sub_hist["Close"].iloc[-1])
                return float(hist["Close"].iloc[0])

            adj_close_1m = get_price_at_date(date_1m)
            adj_close_6m = get_price_at_date(date_6m)
            adj_close_12m = get_price_at_date(date_12m)
            adj_close_36m = get_price_at_date(date_36m)
    except RateLimitExhausted:
        raise
    except Exception as e:
        print(f"Could not fetch historical prices for {ticker_symbol}: {e}")

    # Return all compiled metrics
    return {
        "ticker": ticker_symbol,
        "trailing_pe": (
            round(trailing_pe, 2) if trailing_pe is not None else "N/A"
        ),
        "forward_pe": round(forward_pe, 2) if forward_pe is not None else "N/A",
        "enterprise_value": enterprise_value,
        "dividend_yield": (
            round(dividend_yield * 100, 2) if dividend_yield is not None else "N/A"
        ),
        "fifty_two_week_high": (
            round(fifty_two_week_high, 2) if fifty_two_week_high is not None else "N/A"
        ),
        "fifty_two_week_low": (
            round(fifty_two_week_low, 2) if fifty_two_week_low is not None else "N/A"
        ),
        "price_to_book": (
            round(price_to_book, 2) if price_to_book is not None else "N/A"
        ),
        "total_debt": total_debt if total_debt is not None else "N/A",
        "total_revenue": total_revenue if total_revenue is not None else "N/A",
        "operating_margins": (
            round(operating_margins * 100, 2) if operating_margins is not None else "N/A"
        ),
        "profit_margins": (
            round(profit_margins * 100, 2) if profit_margins is not None else "N/A"
        ),
        "return_on_assets": (
            round(return_on_assets * 100, 2) if return_on_assets is not None else "N/A"
        ),
        "return_on_equity": (
            round(return_on_equity * 100, 2) if return_on_equity is not None else "N/A"
        ),
        "website": website if website else "N/A",
        "cash_and_equivalents": cash_equivalents,
        "short_term_investments": short_term_investments,
        "total_liabilities": total_liabilities,
        "free_cash_flow": free_cash_flow,
        "last_adj_close": last_adj_close,
        "adj_close_1m": adj_close_1m,
        "adj_close_6m": adj_close_6m,
        "adj_close_12m": adj_close_12m,
        "adj_close_36m": adj_close_36m,
    }


def run_pass(tickers):
    results, failed = {}, []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(fetch_ticker_data, t): t for t in tickers}
        for fut in as_completed(futures):
            t = futures[fut]
            try:
                results[t] = fut.result()
            except Exception as e:
                print(f"Failed {t}: {e}")
                failed.append(t)
    return results, failed


if __name__ == "__main__":
    all_results = {}
    pending = tickers_list
    for n in range(1, MAX_PASSES + 1):
        res, pending = run_pass(pending)
        all_results.update(res)
        if not pending:
            break
        if n < MAX_PASSES:
            print(f"{len(pending)} tickers failed; cooling down {PASS_COOLDOWN}s before retry...")
            time.sleep(PASS_COOLDOWN)

    if pending:
        print(f"WARNING: still failed after {MAX_PASSES} passes: {pending}")

    stocks_data = [all_results[t] for t in tickers_list if t in all_results]

    output_data = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "stocks": stocks_data,
    }

    with open("data.json", "w") as f:
        json.dump(output_data, f, indent=4)

    print("Successfully updated data.json with new financial metrics.")
