# Tutorial 1

## Shift Ciphers

In tutorial 1 we deal with shift ciphers 

Exercise 1 deals with Caesar cipher and implementing it with python. To run the script just use 

```
python3 shift-cipher.py
```
Script can look like this with some input
```
Enter the shift number (K): 3
Type 'encrypt' to encrypt or 'decrypt' to decrypt: encrypt
Enter the text: abc
Output: DEF
Time taken: 0.000035 seconds
```

There is also a script to break caesar cipher -

```
python3 break-shift-cipher.py 
Enter the text to decrypt: IYE RKFO NYXO GOVV DY VOKBX DRSC DOMRXSAEO. LED DRSXQ GSVV QOD WYBO NSPPSMEVD - KNWSX
Possible Decryptions:

Key 0: IYE RKFO NYXO GOVV DY VOKBX DRSC DOMRXSAEO. LED DRSXQ GSVV QOD WYBO NSPPSMEVD - KNWSX
Key 1: HXD QJEN MXWN FNUU CX UNJAW CQRB CNLQWRZDN. KDC CQRWP FRUU PNC VXAN MROORLDUC - JMVRW
Key 2: GWC PIDM LWVM EMTT BW TMIZV BPQA BMKPVQYCM. JCB BPQVO EQTT OMB UWZM LQNNQKCTB - ILUQV
Key 3: FVB OHCL KVUL DLSS AV SLHYU AOPZ ALJOUPXBL. IBA AOPUN DPSS NLA TVYL KPMMPJBSA - HKTPU
Key 4: EUA NGBK JUTK CKRR ZU RKGXT ZNOY ZKINTOWAK. HAZ ZNOTM CORR MKZ SUXK JOLLOIARZ - GJSOT
Key 5: DTZ MFAJ ITSJ BJQQ YT QJFWS YMNX YJHMSNVZJ. GZY YMNSL BNQQ LJY RTWJ INKKNHZQY - FIRNS
Key 6: CSY LEZI HSRI AIPP XS PIEVR XLMW XIGLRMUYI. FYX XLMRK AMPP KIX QSVI HMJJMGYPX - EHQMR
Key 7: BRX KDYH GRQH ZHOO WR OHDUQ WKLV WHFKQLTXH. EXW WKLQJ ZLOO JHW PRUH GLIILFXOW - DGPLQ
Key 8: AQW JCXG FQPG YGNN VQ NGCTP VJKU VGEJPKSWG. DWV VJKPI YKNN IGV OQTG FKHHKEWNV - CFOKP
Key 9: ZPV IBWF EPOF XFMM UP MFBSO UIJT UFDIOJRVF. CVU UIJOH XJMM HFU NPSF EJGGJDVMU - BENJO
Key 10: YOU HAVE DONE WELL TO LEARN THIS TECHNIQUE. BUT THING WILL GET MORE DIFFICULT - ADMIN
Key 11: XNT GZUD CNMD VDKK SN KDZQM SGHR SDBGMHPTD. ATS SGHMF VHKK FDS LNQD CHEEHBTKS - ZCLHM
Key 12: WMS FYTC BMLC UCJJ RM JCYPL RFGQ RCAFLGOSC. ZSR RFGLE UGJJ ECR KMPC BGDDGASJR - YBKGL
Key 13: VLR EXSB ALKB TBII QL IBXOK QEFP QBZEKFNRB. YRQ QEFKD TFII DBQ JLOB AFCCFZRIQ - XAJFK
Key 14: UKQ DWRA ZKJA SAHH PK HAWNJ PDEO PAYDJEMQA. XQP PDEJC SEHH CAP IKNA ZEBBEYQHP - WZIEJ
Key 15: TJP CVQZ YJIZ RZGG OJ GZVMI OCDN OZXCIDLPZ. WPO OCDIB RDGG BZO HJMZ YDAADXPGO - VYHDI
Key 16: SIO BUPY XIHY QYFF NI FYULH NBCM NYWBHCKOY. VON NBCHA QCFF AYN GILY XCZZCWOFN - UXGCH
Key 17: RHN ATOX WHGX PXEE MH EXTKG MABL MXVAGBJNX. UNM MABGZ PBEE ZXM FHKX WBYYBVNEM - TWFBG
Key 18: QGM ZSNW VGFW OWDD LG DWSJF LZAK LWUZFAIMW. TML LZAFY OADD YWL EGJW VAXXAUMDL - SVEAF
Key 19: PFL YRMV UFEV NVCC KF CVRIE KYZJ KVTYEZHLV. SLK KYZEX NZCC XVK DFIV UZWWZTLCK - RUDZE
Key 20: OEK XQLU TEDU MUBB JE BUQHD JXYI JUSXDYGKU. RKJ JXYDW MYBB WUJ CEHU TYVVYSKBJ - QTCYD
Key 21: NDJ WPKT SDCT LTAA ID ATPGC IWXH ITRWCXFJT. QJI IWXCV LXAA VTI BDGT SXUUXRJAI - PSBXC
Key 22: MCI VOJS RCBS KSZZ HC ZSOFB HVWG HSQVBWEIS. PIH HVWBU KWZZ USH ACFS RWTTWQIZH - ORAWB
Key 23: LBH UNIR QBAR JRYY GB YRNEA GUVF GRPUAVDHR. OHG GUVAT JVYY TRG ZBER QVSSVPHYG - NQZVA
Key 24: KAG TMHQ PAZQ IQXX FA XQMDZ FTUE FQOTZUCGQ. NGF FTUZS IUXX SQF YADQ PURRUOGXF - MPYUZ
Key 25: JZF SLGP OZYP HPWW EZ WPLCY ESTD EPNSYTBFP. MFE ESTYR HTWW RPE XZCP OTQQTNFWE - LOXTY
Time taken for finding correct key and decryption is: 0.005723 seconds
```
Script works by iterating through all possible keys but since caesar cipher is easy to break the computation is quite fast.

## Double Caesar cipher

Exercise 2 is about Double caesar cipher, which is basically applying caesar cipher again to once encrypted cipher text.

Keys are hardcoded to 13 and 9 but can be changed.

```
python3 double-cipher.py 
Type 'encrypt' to encrypt or 'decrypt' to decrypt: encrypt
Enter the text: abc
Output: WXY
Time taken: 0.000053 seconds
```

## Affine cipher

The affine cipher is a type of substitution cipher that uses a mathematical formula to encrypt and decrypt messages. Each letter in the plaintext is mapped to its numeric equivalent, transformed using a linear equation 
```
E(x) = (ax + b) mod m
```
and then converted back to a letter. Here, a and b are keys, and m is the size of the alphabet. Decryption reverses the process using 
```
D(x) = a⁻¹(x - b) mod m
```
It's simple but easily breakable with frequency analysis.

Script takes input for a and b, and then encrypt or decrypt mode.

```
python3 affince-cipher.py 
Input values for a and b: 5 13
Type 'encrypt' to encrypt or 'decrypt' to decrypt: encrypt
Enter text to encrypt: abc
Output is  NSX
```

## Frequency Analysis

Frequency analysis is a cryptographic technique used to break substitution ciphers by studying the frequency of letters or groups of letters in ciphertext. Since certain letters (e.g., 'E', 'T', 'A' in English) appear more often than others, comparing these frequencies to known language patterns can help deduce the plaintext. This method is effective against ciphers like the Caesar and Affine ciphers, where each letter is consistently substituted

