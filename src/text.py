TEXT = {
    "Frequency is Freedom": [
        """
“Frequency is freedom” is a phrase coined by the urban planner Jarrett Walker that I learned about from the excellent book [Better Buses Better Cities](https://www.goodreads.com/en/book/show/44451608-better-buses-better-cities), and it has helped me articulate why I felt I had a greater sense of freedom when I have lived and traveled abroad. Frequent transit service allowed me to go more places, to go places whenever I wanted to, and to still go places even when I was running late or forgot something (which seems to happen quite a bit). I spent less time waiting, and so I could get moving sooner and to move faster once I was on the go.
        """,
        """
I miss those freedoms, but I used to have those same freedoms here at home in Chicago. When ridership vanished at the beginning of the pandemic the CTA was forced to cut service¹. These days, buses and trains are still running less often as the [CTA struggles to hire enough bus drivers](https://blockclubchicago.org/2022/07/14/cta-leaders-vow-to-fix-unreliable-service-with-more-hiring-improved-train-and-bus-tracking/). My own commute takes twice as long as it used to, which makes going into the office more of pain. I miss the community of the office, but when I do make the trek I find it mostly empty, because [my coworkers also all hate waiting forever for the bus or train](https://www.wsj.com/articles/dreaded-commute-to-the-city-is-keeping-offices-mostly-empty-11653989581).
        """,
    ],

    "How Often Does the Bus Come?": [
        """
Like nearly all transit agencies, the CTA publishes scheduled and realtime service data. While anyone who lives in the city knows that the bus never runs on schedule, we can look at this data to see the service the CTA intends to run. Below is scheduled weekday service from the week of August 15th for two bus stops near my apartment. (I’ve filtered this data to only show service between 6 am and 10 pm, but the CTA does run buses and trains all night on many routes, including the 66 bus shown here.)
        """,
    ],

    "How Often Does the Bus Come? (II)": [
        """
These numbers feel high to me. As expected, both buses have peaks around rush hour, but an average of 9 buses per hour for the 66 bus, which runs down Chicago Ave, feels high to me. That’s one bus nearly every 6 and half minutes. I wish the bus ran that often, because how often the bus comes determines how long I’m stuck waiting for it.
        """,
    ],

    "How Long Do You Wait For The Bus?": [
        """
There are may things in the world of transportation that are counterintuitive, one of them being how long you wait for the bus. If a bus arrives on average every ten minutes, you would be forgiven for thinking that the average time some spends waiting for the bus is half that, only five minutes. This would be the case if the bus arrived exactly every ten minutes, like clockwork, but it doesn’t. It arrives _on average_ every ten minutes, sometime sooner and sometimes later. And, sadly and surprisingly, the average time someone spends waiting for a bus like that is ten minutes.³""",
        """
To understand why, think about a university that advertises small class. Tallying each class, the average may indeed be small, say thirty students. But not every class is that small. A few big freshman seminars may have hundreds of students. And since more students take those larger classes, when we tally students, their average number of students in their classes will be much higher.²
        """,
        """
When choosing a student at random, you are more likely to get a student in a larger class. When a bus arrives at a certain frequency – sometimes shorter, sometimes longer – you are more likely to arrive at the stop during a longer period. This same paradox explains why [your friends have more friends than you](https://towardsdatascience.com/the-inspection-paradox-is-everywhere-2ef1c2e9d709#070e). 
        """,
    ],

    "One Day of Simulated Bus Service": [
        """
To test this, we can simulate a bus and measure how long simulated people have to wait for it. Our simulated bus runs 24 hours a day and the little simulated people show up at all times. (They work inside a computer and never get any time off.)
        """,
],

    "How Far Can I Go?": [
        """
How often the bus comes determines how far it can take me. A bus that runs more frequently is more likely to come on time, since it will bunch less [citation needed]. A bus that runs more frequently will be stuck in less traffic, since every bus carries people who would otherwise be driving [citation needed]. But most acutely, when a bus comes more often I spend less time waiting for it. 
        """,
        """
I want to use the CTA’s own data to measure how far I can go in a certain amount of time. To do that, I first need to map everywhere I can walk to. What you see below is a map of everywhere I can walk within an hour from my apartment, which is near the intersection of Chicago and Damen.
        """,
    ],

    "How Far Can My Feet Carry Me?": [
        """
First, I need to know everywhere I can walk. Using OpenStreetMaps, I can trace everywhere I can walk within one hour of my apartment.
        """,
    ],

    "Geography": [
        """
The map above shows all walking routes surrounding my apartment. I find it quite beautiful how the highway to the east shows up almost like a river that I can only cross at certain spots. Chicago is quite a flat city with no hills or mountains to limit where we can build. Instead, our geography is defined by the transportation networks we build for ourselves.
        """,
    ],

    "Generate Your Own Walking Map": [
        """
Enter an address below to generate a map of everywhere you can walk from that spot. (This will work for any address, but it'll take a few minutes as it'll have to download the map surrounding that address first.)
        """,
    ],

    "How Far Can I Go with Public Transit": [
        """
Now that we can walk, let’s walk to the bus, or, more honestly, let’s wait for the bus. Using the CTA’s publicly available schedule data, we can trace everywhere transit can take us from a given starting point and measure how long it would take to do so. Crucially, from the arrival rates shown above, we also know how long we can expect to wait at each transit stop. So, for every bus or train stop, the CTA’s own schedule data tells us how often buses or trains come and so how long, on average, we would be stuck waiting.
        """,
        """
The maps below consider weekday CTA service from the week of August 15th. Within city limits, starting from my apartment, we trace every transit stop we can walk to, how long we must wait there, all the other transit stops those routes can take us to, and everywhere we can walk to from there, including other routes we can transfer to, after waiting of course.
        """,
    ],

    "How Far Can I Go with Public Transit (II)": [
        """
The map above shows the city that the CTA makes accessible to me. A friend of mine who lives in Ravenswood was surprised to see that his place isn’t on this map, but I wasn’t. I know to bike to his place for dinner, because the bus would take over an hour.
        """,
    ],

    "More Buses Can Take You More Places": [
        """
Truthfully, that map above is aspirational. It’s based off of the CTA’s published schedules, but the CTA has been running reduced service, sometimes as bad as running [half as many trains as the schedule says](https://blockclubchicago.org/2022/06/23/ghost-trains-and-buses-packed-platforms-35-alderpeople-want-city-council-hearing-on-deteriorating-cta-service/). That means waiting even longer.
        """,
        """
When public transit runs less often, our world gets smaller. TKTKTK [Here I'd like to bring in more numbers and point out how the bus does more work than the train, but need some better maps first!]
        """,
    ],

    "Better Bus Service": [
        """
The CTA is [hurting financially because of reduced ridership](https://experience.arcgis.com/experience/037eb95a8daa44f488e48d9afc09c38e), making it harder to run routes as often as advertised. This creates a vicious cycle, as worse service forces would-be riders to find other options. Many people think that those who are dependent upon the bus will take the bus no matter what, because they have no other choice. Even the current head of the CTA, Dorval Carter has said, “The people who have to ride the CTA will ride the CTA.”⁴
        """,
        """
The bus is often stigmatized as only for poor people who cannot afford a car, but that doesn’t measure up against reality. Research across the US has confirmed that transit ridership levels a result of service quality.⁴ People choose the bus when they learn they can rely upon the bus. When they can’t, they – even poor people – figure something else out.
        """,
        """
Something that I loved about Chicago pre-pandemic was that everyone, rich and poor, relied upon public transit. While friends from the suburbs would be too afraid to take the bus, no Chicagoan wasted time with that nonsense, because it was reliable and safe. [That’s no longer the case](https://blockclubchicago.org/2022/04/27/the-cta-boosted-unarmed-security-to-battle-violence-bad-behavior-on-trains-and-buses-but-riders-say-nothing-has-changed/), but the CTA can win us back. Kurt Luhrsen, vice president of bus operations for METRO, Houston’s transit agency, sums it up well: “You provide a good service, you’ll have customers. You don’t, you wont.”⁴
        """,
    ],

    "Citations & Helpful References": [
    """
1. [CTA Leaders Vow To Fix Unreliable Service With More Hiring, Improved Train And Bus Tracking](https://blockclubchicago.org/2022/07/14/cta-leaders-vow-to-fix-unreliable-service-with-more-hiring-improved-train-and-bus-tracking/) from Block Club Chicago
1. [Dreaded Commute to the City Is Keeping Offices Mostly Empty](https://www.wsj.com/articles/dreaded-commute-to-the-city-is-keeping-offices-mostly-empty-11653989581) from The Wall Street Journal
1. [The Waiting Time Paradox, or, Why Is My Bus Always Late?](https://jakevdp.github.io/blog/2018/09/13/waiting-time-paradox/) by Jake VanderPlas
1. [Better Buses, Better Cities: How to Plan, Run, and Win the Fight for Effective Transit](https://www.goodreads.com/en/book/show/44451608-better-buses-better-cities) by Steven Higashide
1. [The Inspection Paradox is Everywhere](https://towardsdatascience.com/the-inspection-paradox-is-everywhere-2ef1c2e9d709) by Allen Downey
1. [Isochrone Maps with OSMnx + Python](https://geoffboeing.com/2017/08/isochrone-maps-osmnx-python/) by Geoff Boeing
1. [The Mobility Database](https://database.mobilitydata.org/) and [GTFS Schedule Reference](https://gtfs.org/schedule/reference/)
1. [Isochrone Maps with R and OpenTripPlanner](https://xang1234.github.io/isochrone/) by David Ten, for his very helpful diagram of the GTFS schema.
1. And lastly, a big thank you to [all my lovely coworkers](https://www.ideo.com/jobs) who helped with this project. You're brilliant and beautiful.
    """,
]

}