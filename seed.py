from app import app
from models import db, Genre

with app.app_context():
    db.drop_all()
    db.create_all()

G1 = Genre(
    name="Rock",
    description='Rock music is a broad genre of popular music that originated as "rock and roll" in the United States in the early 1950s, and developed into a range of different styles in the 1960s and later, particularly in the United States and the United Kingdom. It has its roots in 1940s and 1950s rock and roll, a style which drew heavily from the genres of blues, rhythm and blues, and from country music. Rock music also drew strongly from a number of other genres such as electric blues and folk, and incorporated influences from jazz, classical and other musical styles. Musically, rock has centered on the electric guitar, usually as part of a rock group with electric bass, drums, and one or more singers. Usually, rock is song-based music usually with a 4/4 time signature using a verse-chorus form, but the genre has become extremely diverse. Like pop music, lyrics often stress romantic love but also address a wide variety of other themes that are frequently social or political.',
)
G2 = Genre(
    name="Pop",
    description="Pop music is a genre of popular music that originated in its modern form in the United States and United Kingdom during the mid-1950s. The terms popular music and pop music are often used interchangeably, although the former describes all music that is popular and includes many disparate styles. During the 1950s and 1960s, pop encompassed rock and roll and the youth-oriented styles it influenced. The terms remained roughly synonymous until the late 1960s, after which pop became associated with music that was more commercial, ephemeral, and accessible. Although much of the music that appears on record charts is seen as pop music, the genre is distinguished from chart music. Pop music is eclectic, and often borrows elements from other styles such as urban, dance, rock, Latin, and country; nonetheless, there are core elements that define pop music. Identifying factors include generally short to medium-length songs written in a basic format (often the verse-chorus structure), as well as common use of repeated choruses, melodic tunes, and hooks.",
)
G3 = Genre(
    name="Hip Hop",
    description="Hip Hop music is a genre of music that originated in African American communities in New York City in the 1970s. It consists of a stylized rhythmic music that commonly accompanies rapping, a rhythmic and rhyming speech that is chanted. It developed as part of hip hop culture, a subculture defined by four key stylistic elements: MCing/rapping, DJing/scratching with turntables, break dancing, and graffiti writing. Other elements include sampling beats or bass lines from records (or synthesized beats and sounds), and rhythmic beatboxing. While often used to refer solely to rapping, hip hop more properly denotes the practice of the entire subculture. The term hip hop music is sometimes used synonymously with the term rap music, though rapping is not a required component of hip hop music; the genre may also incorporate other elements of hip hop culture, including DJing, turntablism, scratching, beatboxing, and instrumental tracks.",
)
G4 = Genre(
    name="Country",
    description="Country music is a genre of popular music that originated with blues, old-time music, and various types of American folk music including Appalachian, Cajun, and the cowboy Western music styles of New Mexico, Red Dirt, Tejano, and Texas country. Its popularized roots originate in the Southern United States of the early 1920s. Country music often consists of ballads and dance tunes with generally simple forms, folk lyrics, and harmonies mostly accompanied by string instruments such as banjos, electric and acoustic guitars, steel guitars (such as pedal steels and dobros), and fiddles as well as harmonicas. Blues modes have been used extensively throughout its recorded history. According to Lindsey Starnes, the term country music gained popularity in the 1940s in preference to the earlier term hillbilly music; it came to encompass Western music, which evolved parallel to hillbilly music from similar roots, in the mid-20th century.",
)
G5 = Genre(
    name="Jazz",
    description="Jazz music is a genre of music that originated in the African-American communities of New Orleans, United States, in the late 19th and early 20th centuries, with its roots in blues and ragtime. Since the 1920s Jazz Age, it has been recognized as a major form of musical expression in traditional and popular music, linked by the common bonds of African-American and European-American musical parentage. Jazz is characterized by swing and blue notes, call and response vocals, polyrhythms and improvisation. Jazz has roots in West African cultural and musical expression, and in African-American music traditions including blues and ragtime, as well as European military band music. Intellectuals around the world have hailed jazz as one of America's original art forms.",
)
G6 = Genre(
    name="Classical",
    description="Classical music is art music produced or rooted in the traditions of Western culture, including both liturgical (religious) and secular music. While a more precise term is also used to refer to the period from 1750 to 1820 (the Classical period), this article is about the broad span of time from before the 6th century AD to the present day, which includes the Classical period and various other periods. The central norms of this tradition became codified between 1550 and 1900, which is known as the common-practice period. The major time divisions of Western art music are as follows: the ancient music period, before 500 AD; the early music period, which includes the Medieval (500–1400) including Gregorian chant, and the Renaissance (1400–1600); the common-practice period, which includes Baroque (1600–1750), Classical (1750–1820), and Romantic (1810–1910); the 20th century (1901–2000) which includes the modern (1890–1930) that overlaps from the late-19th century, the high modern (mid 20th-century), and contemporary or postmodern (1975–2000) eras; and the 21st century (2001–present) which includes the contemporary (2000–present) period.",
)
G7 = Genre(
    name="R&B",
    description="R&B music stands for rhythm and blues music. It is a popular music form developed by African Americans incorporating elements of jazz and blues as well as gospel music. Although the term often refers to popular music, the creators of R&B music intended to create a version of the genre that was less pop-oriented and more consistent with the original style of rhythm and blues music. R&B music is characterized by a significant blues influence, simple chord progressions, and a strong back beat. The term was coined in the late 1940s when rhythm and blues music was becoming more popular with African Americans. At that time, the term was used to describe blues-influenced music that was primarily performed by African Americans. Today, the term R&B music is used to describe a wide range of musical styles that are typically performed by African American artists.",
)
G8 = Genre(
    name="Electronic",
    description="Electronic music is music that employs electronic musical instruments, digital instruments, or circuitry-based music technology in its creation. It includes both music made using electronic and electromechanical means (electroacoustic music). Pure electronic instruments depended entirely on circuitry-based sound generation, for instance using devices such as an electronic oscillator, theremin, or synthesizer. Electromechanical instruments can have mechanical parts such as strings, hammers, and electric elements including magnetic pickups, power amplifiers and loudspeakers. Such electromechanical devices include the telharmonium, Hammond organ, electric piano and the electric guitar. Pure electronic instruments are now sometimes preferred over mechanical ones for their wider range of sounds and effects, but because they include mechanical as well as electronic components, they are invariably referred to as electromechanical.",
)
G9 = Genre(
    name="Folk",
    description="Folk music includes traditional folk music and the genre that evolved from it during the 20th-century folk revival. Some types of folk music may be called world music. Traditional folk music has been defined in several ways: as music transmitted orally, music with unknown composers, or music performed by custom over a long period of time. It has been contrasted with commercial and classical styles. The term originated in the 19th century, but folk music extends beyond that. Starting in the mid-20th century, a new form of popular folk music evolved from traditional folk music. This process and period is called the (second) folk revival and reached a zenith in the 1960s. This form of music is sometimes called contemporary folk music or folk revival music to distinguish it from earlier folk forms. Smaller, similar revivals have occurred elsewhere in the world at other times, but the term folk music has typically not been applied to the new music created during those revivals. This type of folk music also includes fusion genres such as folk rock, folk metal, electric folk, and others. While contemporary folk music is a genre generally distinct from traditional folk music, it often shares the same English name, performers and venues as traditional folk music; even individual songs may be a blend of the two.",
)
G10 = Genre(
    name="Reggae",
    description='Reggae music is a genre that originated in Jamaica in the late 1960s. The term also denotes the modern popular music of Jamaica and its diaspora. A 1968 single by Toots and the Maytals, "Do the Reggay" was the first popular song to use the word "reggae", effectively naming the genre and introducing it to a global audience. While sometimes used in a broad sense to refer to most types of popular Jamaican dance music, the term reggae more properly denotes a particular music style that was strongly influenced by traditional mento as well as American jazz and rhythm and blues, especially the New Orleans R&B practiced by Fats Domino and Allen Toussaint, and evolved out of the earlier genres ska and rocksteady. Reggae usually relates news, social gossip, and political comment. Reggae spread into a commercialized jazz field, being known first as "rudie blues", then "ska", later "blue beat", and "rock steady". It is instantly recognizable from the counterpoint between the bass and drum downbeat and the offbeat rhythm section. The immediate origins of reggae were in ska and rocksteady; from the latter, reggae took over the use of the bass as a percussion instrument.',
)
G11 = Genre(
    name="Blues",
    description='Blues music originated in the Deep South of the United States around the 1860s by African-Americans from roots in African musical traditions, African-American work songs, and spirituals. Blues incorporated spirituals, work songs, field hollers, shouts, chants, and rhymed simple narrative ballads. The blues form, ubiquitous in jazz, rhythm and blues and rock and roll, is characterized by the call-and-response pattern, the blues scale and specific chord progressions, of which the twelve-bar blues is the most common. Blue notes (or "worried notes"), usually thirds, fifths or sevenths flattened in pitch are also an essential part of the sound. Blues shuffles or walking bass reinforce the trance-like rhythm and form a repetitive effect known as the groove.',
)
G12 = Genre(
    name="Metal",
    description="Metal music is a genre of rock music that developed in the late 1960s and early 1970s, largely in the United Kingdom and the United States. With roots in blues rock, psychedelic rock, and acid rock, heavy metal bands developed a thick, massive sound, characterized by distortion, extended guitar solos, emphatic beats, and loudness. The lyrics and performances are sometimes associated with aggression and machismo.",
)
G13 = Genre(
    name="Punk",
    description="Punk music is a genre stylized by short, fast-paced songs with hard-edged melodies and singing styles, stripped-down instrumentation, and often political, anti-establishment lyrics. Punk embraces a DIY ethic; many bands self-produce recordings and distribute them through independent record labels and other informal channels.",
)
G14 = Genre(
    name="Progressive Rock",
    description="Progressive Rock music is a genre of rock that originated in the United Kingdom and United States in the late 1960s. The genre developed from psychedelic rock, and originated as an attempt to give greater artistic weight and credibility to rock music. Bands abandoned the short pop single in favor of instrumentation and compositional techniques more frequently associated with jazz or classical music in an effort to give rock music the same level of musical sophistication and critical respect. Long track lengths and odd time signatures are common. While the genre is often cited for its merging of high culture and low culture, few artists incorporated literal classical themes in their work to any great degree, and only a handful of groups purposely emulated or referenced classical music. The genre coincided with the mid 1960s economic boom that was able to support groups of musicians with a higher level of artistic freedom than any generation since the 1920s.",
)
G15 = Genre(
    name="Disco Polo",
    description="Disco Polo is a genre of music originating from Poland in the early 1980s. It is a form of Eurodance and pop music. Its name comes from a popular music genre in the late 1980s, which replaced many of the beat-driven forms of disco music, and which derived from disco, hi-NRG, and Euro disco. Disco polo music is strongly associated with the dance style and associated fashion, hairstyle and make-up. The music is popular in Poland, and is gaining popularity in Ukraine, Belarus and Lithuania.",
)
G16 = Genre(
    name="Sklap",
    hypothetical=True,
    description="Sklap is a genre of music that originated in an a small underground music cult in 2005. The genre consists purely of noises that can be made using only human skin. Mostly clapping and slapping sounds. At first, the genre gained popularity as a meme and people would listen to it ironically. However, as most things that are ironic, it became unironic and people started to listen to it unironically while never admitting they actually like it. The genre is now one of the most popular genres in the world.",
)
with app.app_context():
    db.session.add_all(
        [G1, G2, G3, G4, G5, G6, G7, G8, G9, G10, G11, G12, G13, G14, G15, G16]
    )
    db.session.commit()
