import json
from datetime import datetime
import yfinance as yf

tickers_list = ["ALC", "SMNNY", "SHW", "JNJ", "CRWD", "ABNB", "FTNT", "TEAM", "TRI", "ISRG", "PLTR", "CMCSA", "ORLY", "ARM", "LR", "GEBN", "KNIN", "HOLN", "LONN", "SIEGY", "WRT1V", "KCR.HE", "STE-R", "BVI", "RMS.PA", "BN.PA", "SU.PA", "SPOT", "HNNMY", "INTU", "GWRE", "MNST", "FAST", "ERNXY", "FUR", "AMG.PA", "VPK.AS", "ISS", "DEMANT", "MAERSK-B", "LTMC", "REL", "HWDN", "DOV", "ANET", "APH", "MANH", "IMI1.F", "AOFG", "MCO", "DPZ", "FTNT", "ECL", "EQIX", "KLAC", "COUR", "ISRG", "AMT", "LOTB", "OCI.AS", "BFIT", "CRBN.AS", "AMP.MI", "G1A", "DRW3", "RHM", "UNH", "TRIP", "GIS", "SIKA", "FISV", "SAUHY", "UHR", "BNTGY", "TMRAY", "CAP", "POOL", "EVO.CO", "ATCO-A", "SDVKY", "HEXA-B", "SAAB-B", "ESSITY-B", "MCK", "GDDY", "WIX", "CL", "ADP", "FTV", "TTEK", "WRLD", "ITW", "MTD", "SGO.PA", "ERF", "STZ", "DG", "SIRI", "CROX", "MNDY", "CALY", "HOG", "AMGN", "GS", "IBM", "RIO", "GSK", "NG", "LLOY", "NWG", "KLAC", "APP", "WDC", "BKR", "ALNY", "TTWO", "AVGO", "AXON", "CTAS", "LRCX", "ADI", "AMD", "BKNG", "AEP", "ADBE", "ADP", "GILD", "HON", "CSGP", "INSM", "VZ", "SHW", "AXP", "AMZN", "DIS", "CVX", "JPM", "TRV", "MRK", "MMM", "CON.DE", "ADDYY", "BEI", "EONGY", "ALV.DE", "JTKWY", "RAND.AS", "MT", "IMCD", "AEG", "AKZA", "INGA", "NN.AS", "KPN", "AD.AS", "AALB", "ABN", "ASRNL", "HEIA", "LKFT.AS", "ULVR", "URW", "BNP", "KER", "ORA.PA", "TEP.PA", "VIE", "STM", "CA.PA", "RNO", "PUB", "GLE.PA", "CTAS", "CHTR", "CTSH", "DDOG", "GEHC", "KHC", "WDAY", "XEL", "MU", "MELI", "MDLZ", "ODFL", "PANW", "PCAR", "MPWR", "BAS.DE", "TXN", "ZS", "NXPI", "SMMNY", "BMW", "G24", "SAP", "DB1", "DHLGY", "BAYRY", "RWE", "FME.DE", "VNA", "FRE.DE", "HEN3", "PAH3", "SIE", "AIR.DE", "DTE.DE", "VOW3.DE", "MRK", "MUV2", "DAII", "CARL-B", "NKT.CO", "VWS", "NOVO-B", "PNDORA", "RBREW", "AMBU-B", "ORSTED", "BVNRY", "FLS", "GN", "ROCK-B", "JYSK", "GMAB", "DSV.CO", "DANSKE", "ALSYDB", "TRYG", "ZEAL", "HO", "ACA.PA", "BOUYY", "SAFRY", "CS.PA", "STLA", "TTE", "SAN.PA", "ENGI", "AC.PA", "EL.PA", "INTC", "MCHP", "MRVL", "MSFT", "STX", "ROST", "TMUS", "PDD", "PAYX", "CEG", "CSX", "CCEP", "FANG", "FER", "ROP", "WBD", "REGN", "PEP", "LIN", "KDP", "HNR1", "QIA.F", "HEI", "CBK", "DTG", "SNPS", "TXN", "VRTX", "DXCM", "EXC", "MAR", "META", "MSTR", "GOOGL", "KNIN", "LOGI", "SREN", "SIKA", "SOON", "SCMN", "SMWH", "AMAT", "UBS", "NESN", "NOVN", "ROP.SW", "SLHN", "ZURN", "ABBN", "PGHN", "SKF-B", "ALFA", "EQT", "EPI-A", "ADDT-B", "BOL.ST", "ERIC-B", "TELIA", "SKA-B", "TEL2-B", "TSCO.L", "WEIR", "RTO", "CRDA", "BRBY", "HLMA", "GLEN", "BNZL", "PSON.L", "SGRO.L", "SCA-B", "AZN", "SAND.ST", "VOLCAR-B", "BAB.L", "BA.L", "BP", "ANTO", "SBRY", "SHEL", "KGF", "HLN", "FRES.L", "INF", "JD", "HSX.L", "MNDI", "WTB", "VOD", "STAN", "MKS", "RKT.L", "RACE", "DPLM", "CNA.L", "BT.A", "DCC", "ENT", "PSON", "PSN", "ITX.MC", "AENA.MC", "GRF.MC", "IDR.MC", "MAP.MC", "CLNX.MC", "REP.MC", "LOG.MC", "FDR.MC", "SLR.MC", "MRO", "SVT", "CTEC.L", "ABF", "IAG.L", "IMB", "NXT.L", "BEZ", "SDR.L", "STAN.L", "SDLF", "SSE.L", "UU", "BBOX.L", "STJ", "AAL.L", "ADM.L", "AAF", "BARC", "BLND.L", "CCH", "BKG", "LGEN", "SLB", "SNA", "VLTO", "APD", "BBY", "GEN", "GRMN", "GD", "IBKR", "WM", "VMC", "WST", "SYY", "TPR", "SJM", "SWK", "RL", "RVTY", "RSG", "ALLE", "ALGN", "AFL", "AZO", "AVY", "ANET", "APTV", "BALL", "AKAM", "ALB", "ACN", "BLDR", "BG", "BF.B", "UBER", "TJX", "TSN", "TRMB", "TT", "TYL", "TSCO", "TGT", "ULTA", "SWKS", "STE", "SW", "STLD", "LUV", "STT", "TER", "TXT", "TMO", "UNP", "URI", "WAT", "WAB", "GWW", "SOLV", "PM", "PPG", "RMD", "RTX", "DGX", "ROL", "PWR", "PHM", "VRSN", "VTRS", "YUM", "ZBH", "ZBRA", "WYNN", "ZTS", "XYL", "WSM", "WMB", "TKO", "TTD", "TDY", "TRGP", "SMCI", "SYK", "NDAQ", "NUE", "NVR", "NTAP", "SPG.F", "NDSN", "ZTF", "ANA", "ACX", "PUIG.MC", "ELE.MC", "NTGY.MC", "ROVI.MC", "NCLH", "NOC", "NWSA", "MOS", "MSI", "TAP", "MOH", "OMC", "OKE", "ORLY", "OTIS", "NRG", "PH", "PSKY", "NSC", "ON", "ORCL", "PAYC", "PKG", "PPL", "RCL", "SPGI", "UPS", "UAL", "WTW", "TEL", "TROW", "ROK", "Q", "PNR", "NTRS", "NEM", "LULU", "LOW", "LMT", "MTCH", "MDT", "MGM", "MKC", "MAS", "MRSH", "MLM", "LYB", "MA", "AOS", "ABT", "MO", "A", "AMCR", "ADM", "AME", "BR", "BSX", "WIE", "VOE.VI", "ADRZY", "ATS.VI", "LNZ", "BG.VI", "PAL.VI", "DIE", "MELE", "SOLB", "UMI.BR", "ACKB", "FFARM", "LIGHT", "MICC", "ACOMO", "NEDAP", "TFF", "PL8.F", "SIGCY", "BUCN", "SUN.SW", "IP.MI", "BZU", "NEXPF", "PRY", "GET", "TYRES", "LXS", "DIA.MI", "SESG", "FUTR.L", "WOSG.L", "DWL", "RUI.PA", "HUH1V", "KGX", "AZE", "LISP", "YOU.L", "EVS", "ITP.PA", "INRN", "NOEJ", "KTN.F", "FIE.F", "FPE3", "46176", "NLM", "BC8.F", "KENDR", "VID.MC", "LHA", "MONC", "AVOL", "TUB.PA", "GALD", "DHER", "BMXMF", "BARN", "SALRY", "PNDA", "CPR", "HAG", "HOT", "INDT", "HOLM-B", "PRX", "SECU-B", "TREL-B", "UCB", "ACSAF", "ASM.AS", "BEAN.SW", "MGDDY", "EVD", "EQNR", "EVK", "LDO", "KGSPY", "KBX.F", "KBGGY", "ORKLY", "SGSN", "UMG", "UPM", "VACN", "YARIY", "SCHP.SW", "SRT4.F", "RYAAY", "TEN.MI", "VSURE", "WISE", "WRT1V", "TIT", "TEF", "ERIC-B", "SUBCY", "RXL", "SAGA-B", "PINE", "RED", "NEM", "NBIS", "NESTE", "NHYDY", "KYGA", "KESKOB", "JRONY", "ENX", "FER", "AKRBF", "AER", "AIBG", "AGS", "HSBA", "HBAN.SW", "ENEL.MI", "DSFIR", "EBO.DE", "AYV", "BAMI.MI", "BMED.MI", "BMPS", "ALO", "ABI.BR", "AMUN.PA", "BZU", "DBK", "METSO", "NIBE-B", "NDA-FI", "ORNBV", "OMV", "PST.MI", "PRU", "RAA.F", "RBI", "REC.MI", "SAMPO", "SDZ", "SHB-A", "ADP.PA", "AGS", "ARGX", "BTRW", "BKT.MC", "SAN", "BBVA.MC", "SAB", "BEIJ-B", "BCVN", "1BKW.MI", "BCPN.LS", "BIRG", "CABK", "BPE", "BOL", "AM", "FGR", "ELISA", "EDP", "EMSN.SW", "EDV", "ELI", "DNBBY", "EDPR", "ENI", "FBK", "EXO", "BALD-B", "GALP", "FORTUM", "G", "GECFF", "XGJ.F", "GBLB", "GET", "IBE", "IPSEY", "IG.MI", "INDU-C", "SEB-A", "SRG.MI", "SGSN", "SOF", "SWED-A", "SDLF", "TLX.F", "SREN", "SYENS", "VER", "UU.L", "UNI", "UCG", "TRN", "SPSN", "SOBI", "LIFCO-B", "LUND-B", "LAND", "LEG.F", "MNG.L", "ISP.MI", "LATO-B", "INVE-B", "BAER.SW", "KBC", "LI.PA", "CVC", "COV.PA", "III.L", "I.L", "LSEG", "PEGA", "CIEN", "CVNA", "CI", "CMG", "DECK", "DVA", "EL", "GEV", "JBL", "SNDK", "HOOD", "SPG", "SYF", "PFE", "PCG", "PFG", "PNW", "PSX", "CB", "CHD", "SCHW", "CINF", "CL", "CRL", "CF", "CMS", "CFG", "CMI", "ED", "COP", "COO", "CME", "CLX", "CCI", "CRH", "DLR", "DLTR", "WEC", "IT", "FE", "HRL", "HWM", "PODD", "HUBB", "HST", "BEN", "GPN", "ABX", "CHRW", "CNP", "BRO", "CARR", "BXP", "CBRE", "ACGL", "AIZ", "ABBV", "LNT", "AES", "ARE", "ALL", "ASHM", "BAX", "ATO", "BNY", "XYZ", "BIIB", "CBOE", "COR", "CNC", "CDW", "CPB", "CVS", "CTVA", "DVN", "GLW", "CPAY", "DRI", "DOW", "ETN", "EW", "EPAM", "DUK", "ETR", "EMR", "EME", "ELV", "HAS", "GNRC", "HAL", "GPC", "HCA", "HIG", "GM", "FCX", "FSLR", "BDX", "BMY", "ADP", "TECH", "MET", "MRNA", "LYV", "MTB", "MS", "KEYS", "IR", "JCI", "IFF", "IP", "IVZ", "JKHY", "JBHT", "J", "IQV", "KLAC", "COF", "CPT", "DHI", "DD", "D", "DAL", "DELL", "C", "CAH", "CCL", "BLK", "ERIE", "EFX", "EOG", "EQT", "FDS", "EG", "FDX", "LEN", "KMB", "EXPD", "EXE", "EXPE", "FFIV", "F", "FIS", "FOX", "AJG", "AON", "FIX", "CAG", "EIX", "ESS", "EVRG", "ES", "EXR", "FRT", "IRM", "INVH", "KVUE", "INCY", "KEY", "TPL", "LII", "LW", "KR", "KMI", "LHX", "UDR", "NEE", "NI", "PLD", "O", "RJF", "PNC", "PSA", "PEG", "PGR", "PRU", "BX", "BAC", "BRK.B", "APA", "APO", "ARES", "AMP", "AWK", "AEE", "A", "FITB", "FRT", "HLT", "HUM", "IEX", "HSY", "HPE", "HPQ", "LVS", "LDOS", "KIM", "KKR", "LLY", "MPC", "DVN", "P", "HBAN", "HII", "ICE", "L", "OXY", "T", "COIN", "DTE", "WFC", "WELL", "VICI", "WRB", "VST", "DOC", "MAA", "RF", "REG", "SBAC", "SO", "VTR", "VLO", "UHS", "SRE", "TFC", "GE", "CASY", "COHR", "ECHO", "LITE", "SLB", "GE", "VRT", "QSR", "BN", "HHH", "SEG", "HTZ", "ADT", "AAP", "AAL", "KMX", "CTX", "IPG", "M", "VNO", "VFC", "SIG", "BWA", "ZION", "BFH", "FOSL", "GAP", "AA", "CNX", "VAL", "UNM", "URBN", "GF8A", "SPCX", "NDA-FI", "SWDBY", "SEBA", "LIFCO-B", "INVE-B", "NIBE-B", "INDU-C", "IBE", "UNI", "ACSO", "SCYR", "RED", "ANE", "ENG", "COL.MC", "ICAGY", "MRL", "BGEO", "LMP", "MNG.L", "PSH", "LAND.L", "MTLN", "PCT.L", "SMT", "EDV.L", "IGG", "FERG", "FCIT", "IHG", "ALW", "LSEG", "LIN", "ABI.BR", "ACKB", "SOLB", "LOTB", "SYENS", "UMI.BR", "ELI", "AED", "APAM", "MONT", "AZE", "AGS", "WDP", "MELE", "ARGX", "KESKOB", "MANTA", "HUH1V", "KEMIRA", "TYRES", "BESI.AS", "OUT1V", "VALMT", "KCR", "TIETO", "SSAB-B", "QTCOM", "GBLB", "IBS.LS", "ACJ.F", "NVG.LS", "PHR.LS", "COR.LS", "CTT.LS", "ZEHN", "JEN", "EGL.LS", "SON.LS", "NBA", "RENE", "NOS", "FLO.L", "NORB-B.ST"
]
stocks_data = []

for ticker_symbol in tickers_list:
    ticker = yf.Ticker(ticker_symbol)
    
    # 1. Fetch info dictionary for P/E, EV, Dividend Yield, and Officers
    info = ticker.info
    
    trailing_pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    enterprise_value = info.get("enterpriseValue")
    dividend_yield = info.get("dividendYield") # Usually a decimal like 0.0055 for 0.55%
    total_cash_fallback = info.get("totalCash")
    
    # Extract CEO Name from company officers
    ceo_name = "N/A"
    for officer in info.get("companyOfficers", []):
        title = officer.get("title", "").lower()
        if "ceo" in title or "chief executive officer" in title:
            ceo_name = officer.get("name", "N/A")
            break

    # 2. Get Next Earnings Date from calendar
    next_earnings = "N/A"
    try:
        cal = ticker.calendar
        if cal and "Earnings Date" in cal:
            earnings_dates = cal["Earnings Date"]
            if earnings_dates and len(earnings_dates) > 0:
                next_earnings = str(earnings_dates[0]).split()[0] # Keep date string only
    except Exception as e:
        print(f"Could not fetch earnings date for {ticker_symbol}: {e}")

    # 3. Get Balance Sheet metrics (Cash, Short-Term Investments, Liabilities)
    cash_equivalents = "N/A"
    short_term_investments = "N/A"
    total_liabilities = "N/A"
    
    try:
        bs = ticker.balance_sheet
        if not bs.empty:
            # Cash & Cash Equivalents
            for label in ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        cash_equivalents = float(val)
                        break
            if cash_equivalents == "N/A" and total_cash_fallback is not None:
                cash_equivalents = float(total_cash_fallback)
                
            # Short-Term Investments
            for label in ["Other Short Term Investments", "Short Term Investments"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        short_term_investments = float(val)
                        break
                        
            # Total Liabilities
            for label in ["Total Liabilities Net Minority Interest", "Total Liabilities"]:
                if label in bs.index:
                    val = bs.loc[label].iloc[0]
                    if val is not None and not (isinstance(val, float) and str(val) == "nan"):
                        total_liabilities = float(val)
                        break
    except Exception as e:
        print(f"Could not fetch balance sheet for {ticker_symbol}: {e}")

    # Append all compiled metrics
    stocks_data.append({
        "ticker": ticker_symbol,
        "trailing_pe": round(trailing_pe, 2) if trailing_pe is not None else "N/A",
        "forward_pe": round(forward_pe, 2) if forward_pe is not None else "N/A",
        "ceo": ceo_name,
        "next_earnings": next_earnings,
        "enterprise_value": enterprise_value,
        "dividend_yield": round(dividend_yield * 100, 2) if dividend_yield is not None else "N/A",
        "cash_and_equivalents": cash_equivalents,
        "short_term_investments": short_term_investments,
        "total_liabilities": total_liabilities
    })

output_data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "stocks": stocks_data
}

with open("data.json", "w") as f:
    json.dump(output_data, f, indent=4)

print("Successfully updated data.json with P/E ratios and all metrics.")
