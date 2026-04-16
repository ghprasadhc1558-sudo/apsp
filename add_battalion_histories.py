from app import create_app, db
from app.models.battalion import Battalion

app = create_app()

# Battalion history data
battalion_histories = {
    2: """<h2>HISTORY OF 2ND BATTALION - APSP</h2>

<p>2nd Bn., APSP, was established in the year 1954.</p>

<p>This Battalion was originally raised at Bellary in the composite State of Madras as 3rd Special Armed Police (S.A.P) on 15-12-1947 vide G.O. Ms. No. 4112 Home (D) Dept., Dt: 07-11-1947. The first officer to command this Battalion was Mr. H.G.C. Barboza, an European Officer. The force of the Battalion was initially deployed to curb the Rajakar movement erupted that had then in Tungabhadra river belt area.</p>

<p>After formation of the state of Andhra in the year 1953, this Battalion was shifted from Bellary to Hindupur IMTC Barracks in October 1954 for administrative convenience and the name of SAP was changed to Andhra Special Police. Four companies and two posts of Assistant Commandants were sanctioned to this battalion to enable the battalion's personnel to attend to VIP Bandobust and guard duties at Kurnool. The Battalion was declared to be a permanent establishment vide G.O.Ms.No.2375, Home (Police-C) Department Dated 17.11.1954.</p>

<p>The state of Andhra Pradesh was formed on 1st November 1956. Then the name of the Andhra Special Police was changed to Andhra Pradesh Special Police (APSP) and the Battalion was renumbered as 2nd Bn., APSP vide G.O.Ms.No.1860, Home (Police-B) Dept, Dt 18.11.1957. Later, this Battalion was shifted from Hindupur to Kurnool on 10.05.1959 for administrative convenience.</p>

<p>This Battalion has recently Secured Best contingents Shields on the following occasions:- 1. A.P.S.P Raising Day – 1999 (Best Contingent) 2. Independence Day – 2000 (Best Contingent) 3. AP formation Day – 2002 (Best Contingent) 4. A.P.S.P Raising Day – 2004 (Best Contingent) 5. A.P formation Day – 2006 (Best Contingent) 6. Independence Day – 2012 (Best Contingent) 7. Independence Day – 2013 (Best Contingent) 8. Independence Day – 2021 (Best Contingent) 9. Independence Day – 2022 (2nd Best Armed Contingent)</p>

<p>Officers and men of this unit were awarded various Pathakams in recognition of their distinguished work in their respective fields on various occasions as follows: 1) Utkrisht Seva Pathakam - 08 2) Ati Utkrisht Seva Pathakam - 03 3) Uttama Seva Pathakams - 28 4) Seva Pathakams - 103 5) Katina Seva Pathakam - 02 6) Mahonatha Seva Pathakam - 03 7) Antrik Surksha Seva Padak - 09 8) DGP Commendation Disc - 06</p>""",

    3: """<h2>HISTORY OF 3rd BATTALION - APSP</h2>

<p>The 3rd Battalion APSP is one of the oldest Battalions in the Andhra Pradesh. It was established on 15-12-1947 at Tadepalligudem of West Godavari District. It was then known as 4th Battalion Special Police in the composite Madras State. During the year 1950, this Unit was shifted from Tadepalligudem to Visakhapatnam and it was renamed as Andhra Special Armed Police and renumbered as 3rd Bn. SAP.</p>

<p>After the formation of Andhra Pradesh State in the year 1954, this Battalion was renamed as 3rd Battalion. This Andhra Pradesh Special Police Battalion was later shifted from Visakhapatnam to Kakinada in the year 1962.</p>

<p>This Battalion has the credit of serving in Jammu and Kashmir, Assam and Nagaland for more than 4 years in anti-terrorist operation duties. It has also worked in other state like Tamilnadu, Kerala, Odisha, Chattisgarh, Madhya Pradesh, West Bengal, Uttar Pradesh and Bihar for L&O duties as well as election duties. Nineteen (19) Personnel of this Battalion sacrificed their lives during exchanges of fire with extremists and in land mine blasts planted by extremists.</p>

<p>Sri C.R.Reddy was the first Commandant of this Bn. and he had held this post from 16-1-48 to 5-08-54.</p>

<p>This Unit Contingent received "Best Armed Contingent" Award during Independence Day Celebrations in the years 1991, 1992, 1997, 2000, 2004, 2006, 2007, 2016 & 2017 and "Second Best Armed Contingent" Award in Republic Day parade celebrations in 2005 and Best Armed Contingent for AP Formation Day Parade in 2007. The Battalion personnel have received 05 President Police Medals, 09- Indian Police Medals, 10 Mahonnatha Sevapathakam, 01- Sowryachakra Award, 05-Mukhyamanthri Sourya Pathakams, 504-Uttama Sevapathakams, 228-Sevapathakams---- and 17-Katina Sevapathakams, 16 - Ati Utkrushta Seva Padak, 32 - Utkrushta Seva Padak in recognition of their distinguished service in their respective fields.</p>""",

    5: """<h2>HISTORY OF 5th BATTALION - APSP</h2>

<p>The 5th Battalion was formed on 1.11.1969 at Kakinada vide G.O.Ms.No: 1383 Home (Pol.A) Dept., Dt: 3.10.1969 and was made permanent from 15.3.1975 vide G.O.Ms. No. 1320 Home Dept. Both the 5th Battalion and 5th Bn was shifted to function from Kakinanda. Later 5th Bn was shifted to Vizianagaram Cantonment in October, 1975. The 5th Battalion was completely shifted to Chinthalavalasa in the year 1979 at NH-43 this Battalion is located about 7 KMs. from Vizianagaram(MANSAS TRUST of Maharajas of Vizianagaram) at Chinthalavalasa Village.</p>

<p>These Unit personnel have combated with PWG extremists courageously and killed 35 extremists in several encounters. Unfortunately, 30 police personnel of this Battalion laid down their lives during exchanges of fire/with extremists. The 5th Battalion personnel have secured the following medals and shields at the State and National level Police duty meets. 1) Gold Medals - 06 2) Silver Medals - 04 3) Bronze Medals - 02</p>

<p>Officers and men of this unit were awarded various Pathakams in recognition of their distinguished work in their respective fields on various occasions as follows: 1) IPMs - 07 2) Mukhyamanthri Sourya Pathakams - 06 3) Uttama Seva Pathakams - 36 4) Seva Pathakams - 220 5) Katina Seva Pathakam - 25 6) Police Medal for Gallentary - 01 7) Presidents Police Medal - 01 8) Antrk Surksha Seva Padak - 15 9) Ati- Utkrisht Seva Padak - 12 10 Utkrisht Seva Padak - 25 11) Mahonatha Seva Pathakam - 04 12) DGP Commendation DISC - 12 This Battalion force has performed various duties in various other states like Jammu & Kashmir, Haryana, Tripura, Bihar, Tamilnadu, U.P., and also participated in Cyclone relief & rescue operational duties in Paradeep and Berhampur of Odisha and saved 06 persons during the recent Titli Cyclone and Cyclone in AP.</p>""",

    6: """<h2>HISTORY OF 6th BATTALION - APSP</h2>

<p>6thBn, APSP was established in an area of 142.68 acres at Mangalagiri in Guntur district on 15-09-1972 and the first Commandant of this Bn was Sri S.B.V.Raju. It has its own Firing Range at Undavalli village admeasuring 47.20 Acres. It consists of 7 active companies and one Head Quarter company. The color earmarked for this Battalion is 'Orange' and its logo is 'Lion' worn as shoulder badge representing Palnati Simham.</p>

<p>This Battalion has been engaged in anti - extremist operational duties in the PWG affected districts of Andhra Pradesh. The Battalion was also engaged in Election Bando-Bust duties in the states of Tamilnadu, Karnatka, Kachha Pradesh, Gujarat, Uttar Pradesh, Bihar, Chattisgarh, Rajasthan and Punjab. The Battalion was also engaged in rescue and rehabilitation of flood victims in Orissa state as well as within the state of Andhra Pradesh. The Battalion forces have effectively repulsed the attacks of CPI (Maoists) on Yerragondaplem PS of Prakasam district on 16/17-06-2001 and on Durgi PS of Guntur district on 10-05-2005 while the battalion personnel were performing duties in those Police stations. At present to this battalion is engaged in anti extremist duties, Law and order duties and VIP Security duties in various parts of Andhra Pradesh.</p>

<p>This Bn personnel have been awarded with the following Medals for their outstanding duties: a) 02 MukhyamanthriSouryaPathakams, b) 03 Indian Police Medals, c) 22 A.P.PoliceSevapathakams, d) 09 A.P. UttamaSevapathakams, e) 11 A.P.Katinasevapathakams f) 02 Mahonnatha seva pathakam</p>""",

    9: """<h2>HISTORY OF 9th BATTALION - APSP</h2>

<p>The 9th Bn., APSP, was raised at Vallivedu (Village), Venkatagiri (Mandal) Nellore District on 21.12.1991 with 3 active companies and 1 HQrs Company, this is spread over an area of 303.95 Acres in the present tirupati district out of which 205.10 acres are from Nellore District and 98.85 Acres from Chittoor district which was alienated vide proceedings RC.No.B2/21300/1991 Dt.06.12.1991 (205.10) acres and RC. No.B1/22956/91,Dt.11.05.1993 (98.85 acres) of the District Collector and District Magistrate, Nellore and Chittoor respectively vide GO.MS.No.776 Home (Police-D) Dept. dtd.21.12.1991.Since the establishment of this battalion, this battalion personnel have discharged antiextremist duties/Elections/bandobust duties/Major L&O duties in AP and neighbouring states. This battalion personnel have also conducted lifesaving operations across the state during natural disasters like cyclones.</p>

<p>Officers and men of this unit were awarded various Pathakams in recognition of their distinguished work in their respective fields on various occasions as follows: 1) Utkrisht Seva Pathakam - 09 2) Ati Utkrisht Seva Pathakam - 05 3) Uttama Seva Pathakams - 02 4) Seva Pathakams - 35 5) DGP Commendation Disc - 05</p>""",

    11: """<h2>HISTORY OF 11th BATTALION - APSP</h2>

<p>XI Battalion was initially started as Indian Reserve Police Battalion in 1994 at Tholla Ganganna Palli Village, Vallur Mandal, Kadapa District. Subsequently,This Battalion was shifted to Bhakarapet Village of Sidhout Mandal, Kadapa District on 20-04-1997. This battalion is spreadover an area of 259.5 Acres just beside Kadapa-Tirupathi State Highway on Sidhout-Badvel Road.</p>

<p>This Battalion is functioning with One Hqrs Coy and six Active Companies. This Battalion personnel are performing various bundobust duties within and outside the state they have performed, election duties in the states of Chattisgarh, Punjab, Madya Pradesh, Uttar Pradesh, Gujarat, Karnataka and Tamilnadu. This battalion personnel have also performed rescue and relief operations during cyclones.</p>

<p>This Battalion personnel were awarded a) 48 A P Police Seva Pathakams, b) 13 Uttama Seva Pathkams c) 1 Mahonatha Seva Pathakam. d) 1 PPM. e) 29 Utkrisht Seva Pathakam. f) 13 Ati-Utkrisht Seva Pathakam. g) 07 DGPs Commendation Disc. h) 07 Antrik Suraksha Seva Padak. The Battalion has got four Shields for best performance during Police Parades a) 2006-Republic Day Parade, b) 2009-Independence Day Parade, c) 2010-A.P. Formation Day Parade at Hyderabad d) 2018, Independence day parade at Srikakulam.</p>""",

    14: """<h2>HISTORY OF 14th BATTALION - APSP</h2>

<p>This Battalion has started its functioning w.e.f 01.10.2005 its headquarters was temporarily based at 11th Bn. APSP (IR) Bn. Bhakarapet, Kadapa District with skeletal strength of Head Quarter Coy, two active Coys and 2 platoons in the initial period. Later this Battalion was shifted from 11th Bn. APSP, Bhakrapet, Kadapa District to Ananthapuramu on 17.08.2006. As per the orders of the DGP, A.P., Hyderabad vide Rc.No.60/PL-2/2003, Dt:22.05.08 r/w Endt.Rc.No.27/G/2008 Dt: 06.05.08 of the DIG-III APSP Bns., Kurnool, this Battalion was again shifted temporarily from Ananthapuramu town to Tadipatri. In the year 2014, vide memo No.22127/PS&C/A1/2009, dated: 02.05.2014, the Government of Andhra Pradesh directed to shift 14th Battalion from Tadipatri.</p>

<p>Accordingly, as per the instructions of the Addl.DGP, APSP Bns, Hyderabad vide H.O memo Rc.No.B3/88/2014, dated: 16.05.2014, this unit was shifted from Tadipatri to PTC campus, Ananthapuramu and temporarily accommodated in PTC and DPO Office premises. Subsequently, the Collector and District Magistrate, Ananthapuramu vide office Lr.RC.No.E3/2831/2014, dated: 06.06.2014 sent a proposal to CCLA, AP, Hyderabad. As per the report submitted by the Spl. CS & CCLA, AP, Hyderabad vide Lr.No.Assign.III/16/2014, dated:14.08.2014, the Government of Andhra Pradesh issued orders in G.O.Ms.No.381, Revenue (ASSN.V) Department, dated:14.11.2014 directing the Special Chief Secretary & Chief Commissioner of Land Administration, AP, Hyderabad and the Collector and District Magistrate, Ananthapuramu District to take further necessary action for transferring Government land belonging to Prisons Department to an extent of Acres 118.35 cents in Sy. Nos.254-1, 254-2, 255-1, 255-2, 260, 261, 262, 263 & 256 situated at Janthuluru village, B.K. Samudram Mandal, Ananthapuramu District in favour of the Commandant, 14th (IR) Battalion APSP at Janthuluru village of Ananthapuramu district. This Battalion has secured the following medals: a) DGP Commendation DISC - 04 b) Uttama Sevapathakam - 10 c) Sevapathakams - 28 d) Utkrisht Seva Pathakam - 12 e) Ati- Utkrishth Seva Pathakam - 03 f) 50th Independence Day - 46</p>""",

    16: """<h2>HISTORY OF 16th BATTALION - APSP</h2>

<p>This Battalion was established in the year -2011 Vide G.O.Ms.No. 80, Finance (SMPC-C) Department dated: 05.05.2011 and now the battalion is temporarily situated in District Training Centre, Bakkannapalem, Visakhapatnam. This Battalion has been performing anti extremist duties in Andhra Odisha Border (AOB) area as well as performing police station guard duties and assisting the local police in vehicle checking, local bandobust duties and law and order duties in different parts of the state.</p>

<p>This unit was bagged 1st place and won Trophy in the Ceremonial Parade in connection with Independence Day Celebrations for the year 2018 at Srikakulam District. This unit was bagged 2nd place and won Trophy in Ceremonial Parade in connection with Republic Day Celebrations for the year 2018 at Vijayawada. This unit bagged 1st place and won Trophy in Ceremonial Parade in connection with Independence Day Celebrations for the year 2017 at Taraka Rama Stadium in S.V.University, Tirupathi. as well as in Ceremonial Parade in Independence Day Celebrations 2014 This unit also bagged 1st place and won Trophy in Ceremonial Parade in connection with Republic Day Celebrations for the year 2015 at Vijayawada. This unit Performed Bihar Assembly Election duties in the year 2015 in extremist affected areas in Gaya and Samastipur districts of Bihar State. This unit also performed Election duties in Gujarat in the month of December, 2017. This unit also Participated in one of the contingents along with international participants in the International fleet review celebrations, 2016 at Visakhapatnam. This unit also participated in NDRF demo show, during the year 2016 in front of World Bank's foreign delegates and the union Home Minister Sri Rajanath Singh at Visakhapatnam City. This Battalion has secured the following medals: a) Mahonnatha Seva Pathakam - 01 b) Uttama Sevapathakam - 06 c) Sevapathakams - 36 d) Utkrishth Seva Pathakam - 30 e) Ati- Utkrishth Seva Pathakam - 13 f) DGP Commendation DISC - 03 G) IPM - 01</p>"""
}

with app.app_context():
    try:
        print("Starting to add battalion histories...")
        
        for battalion_number, history_content in battalion_histories.items():
            battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
            
            if battalion:
                battalion.history = history_content
                print(f"✓ Added history for {battalion.name}")
            else:
                print(f"✗ Battalion {battalion_number} not found in database")
        
        db.session.commit()
        print("\n✓ All battalion histories have been successfully added!")
        
        # Verify the updates
        print("\nVerifying updates:")
        for battalion_number in battalion_histories.keys():
            battalion = Battalion.query.filter_by(battalion_number=battalion_number).first()
            if battalion and battalion.history:
                print(f"✓ {battalion.name} - History added (Length: {len(battalion.history)} characters)")
            else:
                print(f"✗ {battalion.name} - History missing")
                
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
