"""Content for The Vijayran Palace site (edit text/images here)."""
LIVE = "https://www.royalquestresorts.com/wp-content/uploads/"
SITE = "https://www.royalquestresorts.com/"
BOOK = "https://staahmax.staah.net/be/indexpackdetail?propertyId=MzEzMA==&individual=true"
PHONE_ROOMS, PHONE_EVENTS = "+91 99998 22609", "+91 99991 63809"
TEL_ROOMS, TEL_EVENTS = "+919999822609", "+919999163809"
EMAIL, EMAIL_SALES = "resv@royalquestresorts.com", "sales@royalquestresorts.com"
ADDRESS = "NH-8, Kukas, Village Kacherawala, Jaipur, Rajasthan 302028, India"
# Exact Sujan fonts (Minion Pro + Brandon Grotesque) via Adobe Fonts.
# Create a Web Project at fonts.adobe.com with "Minion Pro" (Regular 400, Italic) and
# "Brandon Grotesque" (Light 300, Regular 400), then paste the project ID here (e.g. "abc1def").
ADOBE_FONTS_KIT = ""
SOCIAL = [("Instagram", "https://www.instagram.com/vijayranresorts/"), ("Facebook", "https://www.facebook.com/vijayranresorts/"),
          ("YouTube", "https://www.youtube.com/channel/UCkOLuu3C4PpCjX_KS8nZ5zg"), ("Pinterest", "https://in.pinterest.com/vijayranresorts/"),
          ("X", "https://twitter.com/vijayranresorts")]
# ------------------------------------------------------------------ content
ROOMS = [
 dict(slug="presidential-villas", name="Presidential Villas", short="Private pool & garden", count="5 villas",
  hero="2021/05/img01.jpg", panel="2021/05/pv05.png", card="2021/04/Villa-Master-Room.jpg",
  seo="Presidential Villas with Private Pool in Jaipur | The Vijayran Palace",
  desc="Discover true extravagance at our Presidential Villas in Jaipur, each with its own private pool and garden, at The Vijayran Palace heritage resort.",
  lead="Monarch-like comfort, with a private pool and garden of your own.",
  body=["Our Presidential Villas offer a world-class experience of the finest luxuries and supreme comfort. Tasteful interiors, fine tapestry, lavish furniture and aesthetically pleasing art décor take you into a new world, where you cannot help but fall in love with The Vijayran Palace.",
        "Every villa comes with an attached swimming pool and garden, so you can spend your holiday in privacy and luxury amid beautiful surroundings. Traditional charm with monarch-like comfort indeed."],
  facts=["5 villas in this category","Private swimming pool & garden","Living room with sofa-cum-bed","Master bedroom","Spacious shower areas & bathtub","Outdoor garden seating","Mini bar","Air conditioned","Wi-Fi, iron & board on request"],
  gallery=["2021/05/img01.jpg","2021/05/pre02.jpg","2021/05/pv-03.png","2021/05/pv05.png","2021/05/pv04.png"]),
 dict(slug="terrace-haveli-suites", name="Terrace Haveli Suites", short="Sunset terraces & outdoor dining", count="5 suites",
  hero="2021/05/tr-02.jpg", panel="2021/05/tr-01.jpg", card="2021/04/Haveli-Terrace-Suite.jpg",
  seo="Terrace Haveli Suites | Luxury Suites in Jaipur | The Vijayran Palace",
  desc="Classic haveli suites with a sprawling private terrace and outdoor dining area, overlooking the Aravalli hills at The Vijayran Palace, Jaipur.",
  lead="Beautiful sunsets and a view to remember, from your own terrace.",
  body=["Beautiful sunsets, refreshing weather and gorgeous green surroundings: a spectacular view right from the terrace of your Haveli Suite. Embracing the atithi devo bhava (the guest is God) spirit of Indian hospitality, The Vijayran Palace brings you its finest Terrace Haveli Suites.",
        "Each suite is accompanied by a sprawling terrace with an attached outdoor dining area, for a home-away-from-home feel and gorgeous views of the hills."],
  facts=["5 suites available","Private attached terrace","Outdoor seating & dining on the terrace","King-size bed","Air conditioned","Wi-Fi, iron & board on request"],
  gallery=["2021/05/tr-02.jpg","2021/05/ter03.png","2021/05/tr-01.jpg","2021/05/tre05.png","2021/12/rsz_terrace_haveli-min.png"]),
 dict(slug="courtyard-haveli-suites", name="Courtyard Haveli Suites", short="Private garden courtyards", count="11 suites · 1,345 sq ft",
  hero="2021/05/cou-01.jpg", panel="2021/05/cou-02.jpg", card="2021/04/Haveli-Suite-Room.jpg",
  seo="Courtyard Haveli Suites | Family Suites in Jaipur | The Vijayran Palace",
  desc="Grand 1,345 sq ft suites with a private garden courtyard. Old-world charm and modern amenities at The Vijayran Palace, Jaipur.",
  lead="The perfect blend of glorious old-world charm and modern comfort.",
  body=["If you have ever wondered how a king would feel, sitting in a private courtyard beside his majestic room deciding what to have for dinner, the Courtyard Haveli Suite is for you.",
        "We bring you the tranquillity of a rejuvenating getaway with the finest hospitality. A serene evening under a starry sky and fairy lights, dining with your loved ones, is an experience worth splurging on. Every Courtyard Haveli Suite has its own private garden courtyard."],
  facts=["11 suites available","1,345 sq ft each","Private garden courtyard","Outdoor seating","King-size bed","Bathtub","Air conditioned","Wi-Fi, iron & board on request"],
  gallery=["2021/05/cou-01.jpg","2021/05/cou-02.jpg","2021/05/courtyard3.png","2021/05/courtyard4.png","2021/05/courtyard5.png"]),
 dict(slug="balcony-haveli-suites", name="Balcony Haveli Suites", short="Aangan-style courtyards & sunrise views", count="6 suites · 800 sq ft",
  hero="2021/05/bl-03.jpg", panel="2021/05/courtyard5.png", card="2021/04/Balcony-Haveli-Suites.jpg",
  seo="Balcony Haveli Suites | Luxury Resort in Jaipur | The Vijayran Palace",
  desc="800 sq ft Balcony Haveli Suites with a capacious aangan-style courtyard and mountain sunrise views at The Vijayran Palace, Jaipur.",
  lead="Enjoy the drizzle, the breeze and the dawn in an aangan of your own.",
  body=["Our Balcony Haveli Suites are for guests who wish to enjoy the drizzle in a capacious aangan-style courtyard within their own suite. Feel the cool breeze, the mesmerising dusk and the enigma of a lovely dawn.",
        "Rise before the sun, step into the courtyard of your suite, surrounded by mountains, and watch a glorious sunrise unfold right before your eyes. It is more magical than it sounds."],
  facts=["6 suites available","800 sq ft each","Aangan-style private courtyard","King-size bed","Bathtub","Mini bar","Air conditioned","Wi-Fi, iron & board on request"],
  gallery=["2021/05/bl-03.jpg","2021/04/Balcony-Haveli-Suites.jpg","2021/05/courtyard5.png"]),
 dict(slug="jharoka-haveli-suites-2", name="Jharoka Haveli Suites", short="Hand-carved jharokas", count="4 suites · 600 sq ft",
  hero="2021/05/jslide1.jpg", panel="2021/05/jslide22.jpg", card="2021/04/Jharoka-Haveli-Suites.jpg",
  seo="Jharokha Haveli Suites | Resorts in Jaipur for Families | The Vijayran Palace",
  desc="Luxury haveli suites with beautifully carved jharokhas, inspired by Mughal art, at The Vijayran Palace near Jaipur.",
  lead="Step into a Mughal miniature, framed by your own carved jharoka.",
  body=["Remember the Mughal paintings where a queen and her king stand in a beautifully carved jharoka, lost in the sonnets sung by nature? At The Vijayran Palace's Jharoka Haveli Suites, you can be that king or queen.",
        "A beautifully carved jharoka accompanies each luxurious suite, framing breathtaking views of the lush green surroundings, a scene straight out of a period drama and a beautiful setting for photographs."],
  facts=["4 suites available","600 sq ft each","Carved jharoka balcony","King-size bed","Bathtub","Multipurpose table","Electronic safe & mini bar","Air conditioned","Wi-Fi, iron & board on request"],
  gallery=["2021/05/jslide1.jpg","2021/05/jslide22.jpg","2021/05/Jharoka4.png"]),
 dict(slug="haveli-room-twin-bed", name="Haveli Rooms", short="Twin-bed rooms, thoughtfully priced", count="4 rooms · 450 sq ft",
  hero="2021/05/havali.jpg", panel="2021/05/havali012.jpg", card="2021/04/Haveli-Room-with-Twin-Bed.jpg",
  seo="Haveli Rooms with Twin Beds | Heritage Resort Jaipur | The Vijayran Palace",
  desc="Comfortable 450 sq ft Haveli Rooms with twin beds: the heritage luxury of The Vijayran Palace, Jaipur, for every budget.",
  lead="A royal weekend for every budget.",
  body=["We understand that not every holiday is the same, and sometimes you want to steal a weekend for yourself on a limited budget. Our passion for offering spectacular views and warm hospitality to every guest led us to create the Haveli Rooms with twin beds.",
        "Everyone deserves a beautiful, relaxing holiday, and budget should never be the constraint. Welcome to The Vijayran Palace. We await your arrival."],
  facts=["4 rooms available","450 sq ft each","Twin beds","Multipurpose table","Electronic safe & mini bar","Air conditioned","Wi-Fi, iron & board on request"],
  gallery=["2021/05/havali.jpg","2021/05/havali012.jpg"]),
]

EXPERIENCES = [
 ("Morning Yoga", "2021/05/In-Yoga-1.jpg", "Guided morning yoga in our outdoor spaces, with birdsong and the pleasant Aravalli air waiting to embrace you."),
 ("Rajasthani Folk Evenings", "2021/05/rajfolk.jpg", "An evening of music, dance and festivity: the Ravanahatha, Kalbeliya and Ghoomar, performed under the stars."),
 ("Ambar Taal Pool", "2021/06/ambertallpool-img.jpg", "An early-morning swim or a late evening by the pool. Water volleyball for the family and splashing fun for the children."),
 ("Elephant Ride & Lunch", "2021/05/Lunch-with-elephant.jpg", "A short drive into the scenic hills of Amer: feed the elephants, ride through the hills, spot birds and enjoy local delicacies."),
 ("Horse Riding", "2021/06/horse-img.jpg", "Well-trained, friendly horses for a safe and thrilling ride, from pony rides for children to carriage rides for couples."),
 ("Camel Ride", "2021/05/camel-ride.jpg", "Experience the authenticity of Rajasthan on a camel ride through the Aravalli hills."),
 ("Open Jeep Safari", "2021/05/jeep-safari.jpg", "Off-road jeeps take you out to encounter the wild animals and birds of Rajasthan."),
 ("Heritage & Village Walks", "2021/05/jaipur.jpg", "Walk to nature and village life near Amber Fort and Nahargarh, and discover the traditions of rural Rajasthan."),
 ("Bird Watching", "2021/05/bird.jpg", "More than 150 varieties of birds in their natural habitat: a quiet joy for every nature lover."),
]

ATTRACTIONS = [
 ("Amber Fort", "2021/05/AmberFort.jpg", "Explore the rich traditions of the Rajput rulers at Amber Fort, close to The Vijayran Palace. The fort still stands as a perfect picture of ancient Indian architecture."),
 ("Hawa Mahal", "2021/05/HawaMahal.jpg", "The 'Palace of Winds', a five-storey façade shaped like a crown, is Jaipur's most famous landmark and a window into the heritage of the Rajputs."),
 ("City Palace", "2021/05/CityPalace.jpg", "A delightful fusion of Mughal and Rajasthani architecture covering nearly a seventh of the walled city. Don't miss the City Palace Museum."),
 ("Birla Lakshmi Narayan Temple", "2021/05/NarayanTemple.jpg", "Built of white marble, Birla Mandir dominates the skyline of south Jaipur."),
 ("Gaitore Cenotaphs", "2021/05/Gaitore.jpg", "The royal cremation ground of the Kachhwaha kings, set in a narrow valley on the Jaipur–Amer road, with exquisite chhatris in Rajput style."),
]

DINING = [
 ("Fine Dining", "2021/05/dining-01.jpg", "Our restaurant speaks of a bygone regal era through its tastefully decorated interiors, fine tapestry and exquisite miniature artwork, one of Rajasthan's finest gifts to art."),
 ("Dinner under the Sky", "2021/05/dining-02.jpg", "A magical evening under the stars, with a lavish spread of delicacies and the scent of evening primroses."),
 ("In-Room Dining", "2021/05/dining-3.jpg", "After a long day of activities and sightseeing, pick up the menu and our kitchen will bring a lavish dinner to your room."),
 ("A Curated Romantic Dinner", "2021/05/dining-04.jpg", "Tables strewn with roses, aromatic candles and candlelight with a Mughal-e-Azam feel. Let us know a day in advance."),
 ("Poolside Dinner", "2021/05/dining-05.jpg", "A scrumptious dinner by the pool, a gentle breeze and the cherished company of the people you love."),
]

VENUES = [("Vijayran Mahal Bagh","1,000–1,500","Front lawn"),("Rang Mahal","400–500","Inbuilt stage with heritage backdrop & gardens"),
          ("Raj Mahal","250–300","Grand banquet"),("Char Bagh","200–250","Fountain square"),("Trantal","150–200","Main swimming pool area"),
          ("Royal Courtyard","100–150","Banquet hall / fountain area"),("Haveli Chowk","100–150","Haveli central area")]

GALLERY = ["2021/06/Main-Gate.jpg","2021/06/g2.jpg","2021/06/g3.jpg","2021/06/g4.jpg","2021/06/g5.jpg","2021/06/g6.jpg","2021/06/g7-scaled.jpg",
           "2021/06/g8.jpg","2021/06/g9.jpg","2021/06/g10.jpg","2021/06/g11.jpg"]
GALLERY_ALT = ["Main gate of The Vijayran Palace","Destination wedding at The Vijayran Palace","The Vijayran Palace by Royal Quest Resorts","Wedding at The Vijayran Palace",
               "Wedding celebrations at The Vijayran Palace","Wedding venue, The Vijayran Palace","Heritage architecture at The Vijayran Palace","Pre-wedding shoot location",
               "Day outing at The Vijayran Palace","Wedding palace in Rajasthan","Pre-wedding shoot at The Vijayran Palace"]

FAQ = [
 ("Where exactly is The Vijayran Palace?", "In Kukas, on NH-8 near Jaipur, in the Aravalli hills about 12 km north of Amber Fort. Address: " + ADDRESS + "."),
 ("What are the check-in and check-out times?", "Check-in is at 2:00 PM and check-out is at 11:00 AM."),
 ("How do I reserve my accommodation?", "Book online through our reservation engine or call us directly. A reservation is confirmed once the advance payment is received; you may then email us the payment details."),
 ("What is the booking and cancellation policy?", "100% advance payment must be received 10 days before the check-in date. Cancellations made within 10 days of check-in are charged 100% and are non-refundable."),
 ("What payment methods are accepted?", "Cash, credit card, debit card and bank transfer. Travellers' cheques and personal cheques are not accepted."),
 ("Is vegetarian food available?", "Yes, a wide selection of vegetarian dishes is available at our restaurant, and we can prepare Jain meals on request."),
 ("Is there Wi-Fi?", "Yes, Wi-Fi is available across the resort and you are welcome to work from your room."),
 ("What safety precautions apply during safaris?", "Adventure activities carry inherent risk, and The Vijayran Palace accepts no liability arising from them. Please bring your own hat for jeep and camel safaris and keep children supervised."),
]

REVIEWS = [
 ("Perfect place to spend your weekend far from the city's chaotic life. Beautiful property, helpful staff and amazing food. A Presidential Villa with a private pool and lawn is icing on the cake.", "Noopur Sharma"),
 ("We are so glad to have had such a positive experience at this heritage palace. The room was spacious with a beautiful view of the hills. Beautiful looking, and great hospitality.", "Amandeep Kaur"),
 ("A venue for a destination marriage that feels like a dream come true. Beautiful lawns, well-appointed rooms and an old traditional look with all modern amenities.", "Nidhi B"),
]

