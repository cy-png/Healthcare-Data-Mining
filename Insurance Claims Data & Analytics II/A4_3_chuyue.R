library(sandwich)
library(plm)
library(lmtest)
library(stargazer)
library(tidyverse)
library(knitr)
library(car)
library(readr)
library(dplyr)
library(reshape2)
library(data.table)
library(readxl)


VTINP16_upd <- read_csv("Documents/Brandeis/Healthcare Data Analytics/Assignment4/VTINP16_upd.TXT")
View(VTINP16_upd)

# Filter your hospital admissions to only important DRGs between 20 and 977
as.numeric(VTINP16_upd$DRG)
VTINP16_upd_DRG <- VTINP16_upd[VTINP16_upd$DRG >= 20,] 
VTINP16_upd_DRG <- VTINP16_upd_DRG[VTINP16_upd_DRG$DRG <= 977,]
summary(VTINP16_upd_DRG$DRG)
View(VTINP16_upd_DRG)

# Link your filtered Inpatient data to the Revenue Code file using the UNIQ variable
VTREVCODE16 <- read_csv("Documents/Brandeis/Healthcare Data Analytics/Assignment4/VTREVCODE16.TXT")
View(VTREVCODE16)
REVCODE_INP <- merge(VTREVCODE16, VTINP16_upd_DRG, by.x = "Uniq", by.y = "UNIQ")
View(REVCODE_INP)

# Exclude the low dollar value services (less than $100) by dropping the REVCHRGS <100
REVCODE_INP_high <- REVCODE_INP[REVCODE_INP$REVCHRGS >= 100,]
View(REVCODE_INP_high)

# Sum all the charges by the PCCR category
REVCODE_INP_high_useful <- REVCODE_INP_high[,c(1, 7, 10, 89)]
View(REVCODE_INP_high_useful)
groupPCCR <- REVCODE_INP_high_useful %>% group_by(Uniq, DRG, PCCR) %>% summarise(revchrgs = sum(REVCHRGS))
View(groupPCCR)

# cross-tablulate
PCCRcodes <- read_excel("Documents/Brandeis/Healthcare Data Analytics/Assignment4/PCCRcodes.xlsx")
View(PCCRcodes)
groupPCCR_name <- merge(groupPCCR, PCCRcodes, by = "PCCR")
groupPCCR_name <- groupPCCR_name[,-1]
View(groupPCCR_name) #replace PCCR with names

DRGcodes <- read_excel("Documents/Brandeis/Healthcare Data Analytics/Assignment4/DRGcodes.xlsx")
View(DRGcodes)   
groupDRG_name <- merge(DRGcodes, groupPCCR_name, by = "DRG")
DRG_NAME <- paste(groupDRG_name[,1], groupDRG_name[,2], sep=" ")
groupDRG_name_new <- data.frame(DRG_NAME, groupDRG_name)
groupDRG_name_new <- groupDRG_name_new[,-c(2:3)]
View(groupDRG_name_new) # reolace DRG with names

names(groupDRG_name_new)[names(groupDRG_name_new)=="revchrgs"]="value"
cross_tablulate <- dcast(groupDRG_name_new, DRG_NAME ~ PCCR_NAME, mean) # 687 rows and 55 columns
rownames(cross_tablulate) <- cross_tablulate[,1]
cross_tablulate <- cross_tablulate[,-1]
View(cross_tablulate) # 687 rows and 54 columns

# Combining the PCCR 3700 Operating Room + PCCR 4000 Anesthesiology
cross_tablulate$PCCR_OR_and_Anesth_Costs <- cross_tablulate$'Operating Room' + cross_tablulate$Anesthesiology
View(cross_tablulate)

# Turn all those empty cells to zero dollars
cross_tablulate[is.na(cross_tablulate)] = 0
View(cross_tablulate) #687 rows and 55 columns

# write data
write.csv(cross_tablulate,"Documents/Brandeis/Healthcare Data Analytics/Assignment4/cross_tablulate.csv")
