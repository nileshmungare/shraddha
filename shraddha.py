{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "VwK5-9FIB-lu"
      },
      "source": [
        "# Natural Language Processing"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "X1kiO9kACE6s"
      },
      "source": [
        "## Importing the libraries"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 14,
      "metadata": {
        "colab": {},
        "colab_type": "code",
        "id": "7QG7sxmoCIvN"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "import matplotlib.pyplot as plt\n",
        "import pandas as pd"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "wTfaCIzdCLPA"
      },
      "source": [
        "## Importing the dataset"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 15,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "                                                Review  Liked\n",
            "0                             Wow... Loved this place.      1\n",
            "1                                   Crust is not good.      0\n",
            "2            Not tasty and the texture was just nasty.      0\n",
            "3    Stopped by during the late May bank holiday of...      1\n",
            "4    The selection on the menu was great and so wer...      1\n",
            "..                                                 ...    ...\n",
            "995  I think food should have flavor and texture an...      0\n",
            "996                           Appetite instantly gone.      0\n",
            "997  Overall I was not impressed and would not go b...      0\n",
            "998  The whole experience was underwhelming, and I ...      0\n",
            "999  Then, as if I hadn't wasted enough of my life ...      0\n",
            "\n",
            "[1000 rows x 2 columns]\n"
          ]
        }
      ],
      "source": [
        "data = pd.read_csv('Restaurant_Reviews.tsv',delimiter='\\t',quoting=3)\n",
        "#delimiter is set to tab as the dataset is a tsv - tab seperated values\n",
        "#quoting = 3 eliminates any quotes in the file so that our model can process it properly\n",
        "print(data)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "Qekztq71CixT"
      },
      "source": [
        "## Cleaning the texts"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "re library can be used to remove punctuations with the help of sub function, lowercase all characters with lower function, splits sentence into different words using split function\n",
        "\n",
        "nltk is used to remove stop words - these words are not useful in predictions. Some examples of stop words are - the, a, and, etc.\n",
        "\n",
        "PorterStemmer is used for stemming purposes - stemming refers to removing any conjugations of words and keeping all in present tense so that sparse matrix i.e. bag of words can be as optimised as possible\n",
        "\n",
        "Example: Consider there is a review - \"I loved the food\". The loved can be simplified as love because \"I love the food\" also means the same and we can reduce the size of sparse matrix i.e. bag of words."
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 16,
      "metadata": {},
      "outputs": [
        {
          "name": "stderr",
          "output_type": "stream",
          "text": [
            "[nltk_data] Error loading stopwords: <urlopen error [WinError 10060] A\n",
            "[nltk_data]     connection attempt failed because the connected party\n",
            "[nltk_data]     did not properly respond after a period of time, or\n",
            "[nltk_data]     established connection failed because connected host\n",
            "[nltk_data]     has failed to respond>\n"
          ]
        }
      ],
      "source": [
        "import re\n",
        "import nltk\n",
        "\n",
        "nltk.download('stopwords')\n",
        "from nltk.corpus import stopwords\n",
        "from nltk.stem.porter import PorterStemmer\n",
        "\n",
        "corpus = []\n",
        "for i in range(0,len(data)):\n",
        "    review = re.sub('[^a-zA-Z]',' ',data['Review'][i])\n",
        "    review = review.lower()\n",
        "    review = review.split()\n",
        "    ps = PorterStemmer()\n",
        "    all_stopwords = stopwords.words('english')\n",
        "    all_stopwords.remove('not')\n",
        "    review = [ps.stem(word) for word in review if not word in set(all_stopwords)]\n",
        "    review = ' '.join(review)\n",
        "    corpus.append(review)"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 17,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "['wow love place', 'crust not good', 'not tasti textur nasti', 'stop late may bank holiday rick steve recommend love', 'select menu great price', 'get angri want damn pho', 'honeslti tast fresh', 'potato like rubber could tell made ahead time kept warmer', 'fri great', 'great touch', 'servic prompt', 'would not go back', 'cashier care ever say still end wayyy overpr', 'tri cape cod ravoli chicken cranberri mmmm', 'disgust pretti sure human hair', 'shock sign indic cash', 'highli recommend', 'waitress littl slow servic', 'place not worth time let alon vega', 'not like', 'burritto blah', 'food amaz', 'servic also cute', 'could care less interior beauti', 'perform', 'right red velvet cake ohhh stuff good', 'never brought salad ask', 'hole wall great mexican street taco friendli staff', 'took hour get food tabl restaur food luke warm sever run around like total overwhelm', 'worst salmon sashimi', 'also combo like burger fri beer decent deal', 'like final blow', 'found place accid could not happier', 'seem like good quick place grab bite familiar pub food favor look elsewher', 'overal like place lot', 'redeem qualiti restaur inexpens', 'ampl portion good price', 'poor servic waiter made feel like stupid everi time came tabl', 'first visit hiro delight', 'servic suck', 'shrimp tender moist', 'not deal good enough would drag establish', 'hard judg whether side good gross melt styrofoam want eat fear get sick', 'posit note server attent provid great servic', 'frozen puck disgust worst peopl behind regist', 'thing like prime rib dessert section', 'bad food damn gener', 'burger good beef cook right', 'want sandwich go firehous', 'side greek salad greek dress tasti pita hummu refresh', 'order duck rare pink tender insid nice char outsid', 'came run us realiz husband left sunglass tabl', 'chow mein good', 'horribl attitud toward custom talk one custom enjoy food', 'portion huge', 'love friendli server great food wonder imagin menu', 'heart attack grill downtown vega absolut flat line excus restaur', 'not much seafood like string pasta bottom', 'salad right amount sauc not power scallop perfectli cook', 'rip banana not rip petrifi tasteless', 'least think refil water struggl wave minut', 'place receiv star appet', 'cocktail handmad delici', 'definit go back', 'glad found place', 'great food servic huge portion give militari discount', 'alway great time do gringo', 'updat went back second time still amaz', 'got food appar never heard salt batter fish chewi', 'great way finish great', 'deal includ tast drink jeff went beyond expect', 'realli realli good rice time', 'servic meh', 'took min get milkshak noth chocol milk', 'guess known place would suck insid excalibur use common sens', 'scallop dish quit appal valu well', 'time bad custom servic', 'sweet potato fri good season well', 'today second time lunch buffet pretti good', 'much good food vega feel cheat wast eat opportun go rice compani', 'come like experienc underwhelm relationship parti wait person ask break', 'walk place smell like old greas trap other eat', 'turkey roast beef bland', 'place', 'pan cake everyon rave tast like sugari disast tailor palat six year old', 'love pho spring roll oh yummi tri', 'poor batter meat ratio made chicken tender unsatisfi', 'say food amaz', 'omelet die', 'everyth fresh delici', 'summari larg disappoint dine experi', 'like realli sexi parti mouth outrag flirt hottest person parti', 'never hard rock casino never ever step forward', 'best breakfast buffet', 'say bye bye tip ladi', 'never go', 'back', 'food arriv quickli', 'not good', 'side cafe serv realli good food', 'server fantast found wife love roast garlic bone marrow ad extra meal anoth marrow go', 'good thing waiter help kept bloddi mari come', 'best buffet town price cannot beat', 'love mussel cook wine reduct duck tender potato dish delici', 'one better buffet', 'went tigerlilli fantast afternoon', 'food delici bartend attent person got great deal', 'ambienc wonder music play', 'go back next trip', 'sooooo good', 'real sushi lover let honest yama not good', 'least min pass us order food arriv busi', 'realli fantast thai restaur definit worth visit', 'nice spici tender', 'good price', 'check', 'pretti gross', 'better atmospher', 'kind hard mess steak', 'although much like look sound place actual experi bit disappoint', 'know place manag serv blandest food ever eaten prepar indian cuisin', 'worst servic boot least worri', 'servic fine waitress friendli', 'guy steak steak love son steak best worst place said best steak ever eaten', 'thought ventur away get good sushi place realli hit spot night', 'host staff lack better word bitch', 'bland not like place number reason want wast time bad review leav', 'phenomen food servic ambianc', 'return', 'definit worth ventur strip pork belli return next time vega', 'place way overpr mediocr food', 'penn vodka excel', 'good select food includ massiv meatloaf sandwich crispi chicken wrap delish tuna melt tasti burger', 'manag rude', 'delici nyc bagel good select cream chees real lox caper even', 'great subway fact good come everi subway not meet expect', 'serious solid breakfast', 'one best bar food vega', 'extrem rude realli mani restaur would love dine weekend vega', 'drink never empti made realli great menu suggest', '', 'waiter help friendli rare check us', 'husband ate lunch disappoint food servic', 'red curri much bamboo shoot tasti', 'nice blanket moz top feel like done cover subpar food', 'bathroom clean place well decor', 'menu alway chang food qualiti go servic extrem slow', 'servic littl slow consid serv peopl server food come slow pace', 'give thumb', 'watch waiter pay lot attent tabl ignor us', 'fianc came middl day greet seat right away', 'great restaur mandalay bay', 'wait forti five minut vain', 'crostini came salad stale', 'highlight great qualiti nigiri', 'staff friendli joint alway clean', 'differ cut piec day still wonder tender well well flavor', 'order voodoo pasta first time realli excel pasta sinc go gluten free sever year ago', 'place good', 'unfortun must hit bakeri leftov day everyth order stale', 'came back today sinc reloc still not impress', 'seat immedi', 'menu divers reason price', 'avoid cost', 'restaur alway full never wait', 'delici', 'place hand one best place eat phoenix metro area', 'go look good food', 'never treat bad', 'bacon hella salti', 'also order spinach avocado salad ingredi sad dress liter zero tast', 'realli vega fine dine use right menu hand ladi price list', 'waitress friendli', 'lordi khao soi dish not miss curri lover', 'everyth menu terrif also thrill made amaz accommod vegetarian daughter', 'perhap caught night judg review not inspir go back', 'servic leav lot desir', 'atmospher modern hip maintain touch cozi', 'not weekli haunt definit place come back everi', 'liter sat minut one ask take order', 'burger absolut flavor meat total bland burger overcook charcoal flavor', 'also decid not send back waitress look like verg heart attack', 'dress treat rude', 'probabl dirt', 'love place hit spot want someth healthi not lack quantiti flavor', 'order lemon raspberri ice cocktail also incred', 'food suck expect suck could imagin', 'interest decor', 'realli like crepe station', 'also serv hot bread butter home made potato chip bacon bit top origin good', 'watch prepar delici food', 'egg roll fantast', 'order arriv one gyro miss', 'salad wing ice cream dessert left feel quit satisfi', 'not realli sure joey vote best hot dog valley reader phoenix magazin', 'best place go tasti bowl pho', 'live music friday total blow', 'never insult felt disrespect', 'friendli staff', 'worth drive', 'heard good thing place exceed everi hope could dream', 'food great serivc', 'warm beer help', 'great brunch spot', 'servic friendli invit', 'good lunch spot', 'live sinc first last time step foot place', 'worst experi ever', 'must night place', 'side delish mix mushroom yukon gold pure white corn beateou', 'bug never show would given sure side wall bug climb kitchen', 'minut wait salad realiz come time soon', 'friend love salmon tartar', 'go back', 'extrem tasti', 'waitress good though', 'soggi not good', 'jamaican mojito delici', 'small not worth price', 'food rich order accordingli', 'shower area outsid rins not take full shower unless mind nude everyon see', 'servic bit lack', 'lobster bisqu bussel sprout risotto filet need salt pepper cours none tabl', 'hope bode go busi someon cook come', 'either cold not enough flavor bad', 'love bacon wrap date', 'unbeliev bargain', 'folk otto alway make us feel welcom special', 'main also uninspir', 'place first pho amaz', 'wonder experi made place must stop whenev town', 'food bad enough enjoy deal world worst annoy drunk peopl', 'fun chef', 'order doubl cheeseburg got singl patti fall apart pictur upload yeah still suck', 'great place coupl drink watch sport event wall cover tv', 'possibl give zero star', 'descript said yum yum sauc anoth said eel sauc yet anoth said spici mayo well none roll sauc', 'say would hardest decis honestli dish tast suppos tast amaz', 'not roll eye may stay not sure go back tri', 'everyon attent provid excel custom servic', 'horribl wast time money', 'dish quit flavour', 'time side restaur almost empti excus', 'busi either also build freez cold', 'like review said pay eat place', 'drink took close minut come one point', 'serious flavor delight folk', 'much better ayc sushi place went vega', 'light dark enough set mood', 'base sub par servic receiv effort show gratitud busi go back', 'owner realli great peopl', 'noth privileg work eat', 'greek dress creami flavor', 'overal think would take parent place made similar complaint silent felt', 'pizza good peanut sauc tasti', 'tabl servic pretti fast', 'fantast servic', 'well would given godfath zero star possibl', 'know make', 'tough short flavor', 'hope place stick around', 'bar vega not ever recal charg tap water', 'restaur atmospher exquisit', 'good servic clean inexpens boot', 'seafood fresh gener portion', 'plu buck', 'servic not par either', 'thu far visit twice food absolut delici time', 'good year ago', 'self proclaim coffe cafe wildli disappoint', 'veggitarian platter world', 'cant go wrong food', 'beat', 'stop place madison ironman friendli kind staff', 'chef friendli good job', 'better not dedic boba tea spot even jenni pho', 'like patio servic outstand', 'goat taco skimp meat wow flavor', 'think not', 'mac salad pretti bland not get', 'went bachi burger friend recommend not disappoint', 'servic stink', 'wait wait', 'place not qualiti sushi not qualiti restaur', 'would definit recommend wing well pizza', 'great pizza salad', 'thing went wrong burn saganaki', 'wait hour breakfast could done time better home', 'place amaz', 'hate disagre fellow yelper husband disappoint place', 'wait hour never got either pizza mani around us came later', 'know slow', 'staff great food delish incred beer select', 'live neighborhood disappoint back conveni locat', 'know pull pork could soooo delici', 'get incred fresh fish prepar care', 'go gave star rate pleas know third time eat bachi burger write review', 'love fact everyth menu worth', 'never dine place', 'food excel servic good', 'good beer drink select good food select', 'pleas stay away shrimp stir fri noodl', 'potato chip order sad could probabl count mani chip box probabl around', 'food realli bore', 'good servic check', 'greedi corpor never see anoth dime', 'never ever go back', 'much like go back get pass atroci servic never return', 'summer dine charm outdoor patio delight', 'not expect good', 'fantast food', 'order toast english muffin came untoast', 'food good', 'never go back', 'great food price high qualiti hous made', 'bu boy hand rude', 'point friend basic figur place joke mind make publicli loudli known', 'back good bbq lighter fare reason price tell public back old way', 'consid two us left full happi go wrong', 'bread made hous', 'downsid servic', 'also fri without doubt worst fri ever', 'servic except food good review', 'coupl month later return amaz meal', 'favorit place town shawarrrrrrma', 'black eye pea sweet potato unreal', 'disappoint', 'could serv vinaigrett may make better overal dish still good', 'go far mani place never seen restaur serv egg breakfast especi', 'mom got home immedi got sick bite salad', 'server not pleasant deal alway honor pizza hut coupon', 'truli unbeliev good glad went back', 'fantast servic pleas atmospher', 'everyth gross', 'love place', 'great servic food', 'first bathroom locat dirti seat cover not replenish plain yucki', 'burger got gold standard burger kind disappoint', 'omg food delicioso', 'noth authent place', 'spaghetti noth special whatsoev', 'dish salmon best great', 'veget fresh sauc feel like authent thai', 'worth drive tucson', 'select probabl worst seen vega none', 'pretti good beer select', 'place like chipotl better', 'classi warm atmospher fun fresh appet succul steak basebal steak', 'star brick oven bread app', 'eaten multipl time time food delici', 'sat anoth ten minut final gave left', 'terribl', 'everyon treat equal special', 'take min pancak egg', 'delici', 'good side staff genuin pleasant enthusiast real treat', 'sadli gordon ramsey steak place shall sharpli avoid next trip vega', 'alway even wonder food delici', 'best fish ever life', 'bathroom next door nice', 'buffet small food offer bland', 'outstand littl restaur best food ever tast', 'pretti cool would say', 'definit turn doubt back unless someon els buy', 'server great job handl larg rowdi tabl', 'find wast food despic food', 'wife lobster bisqu soup lukewarm', 'would come back sushi crave vega', 'staff great ambianc great', 'deserv star', 'left stomach ach felt sick rest day', 'drop ball', 'dine space tini elegantli decor comfort', 'custom order way like usual eggplant green bean stir fri love', 'bean rice mediocr best', 'best taco town far', 'took back money got outta', 'interest part town place amaz', 'rude inconsider manag', 'staff not friendli wait time serv horribl one even say hi first minut', 'back', 'great dinner', 'servic outshin definit recommend halibut', 'food terribl', 'never ever go back told mani peopl happen', 'recommend unless car break front starv', 'come back everi time vega', 'place deserv one star food', 'disgrac', 'def come back bowl next time', 'want healthi authent ethic food tri place', 'continu come ladi night andddd date night highli recommend place anyon area', 'sever time past experi alway great', 'walk away stuf happi first vega buffet experi', 'servic excel price pretti reason consid vega locat insid crystal shop mall aria', 'summar food incred nay transcend noth bring joy quit like memori pneumat condiment dispens', 'probabl one peopl ever go ian not like', 'kid pizza alway hit lot great side dish option kiddo', 'servic perfect famili atmospher nice see', 'cook perfect servic impecc', 'one simpli disappoint', 'overal disappoint qualiti food bouchon', 'account know get screw', 'great place eat remind littl mom pop shop san francisco bay area', 'today first tast buldogi gourmet hot dog tell ever thought possibl', 'left frustrat', 'definit soon', 'food realli good got full petti fast', 'servic fantast', 'total wast time', 'know kind best ice tea', 'come hungri leav happi stuf', 'servic give star', 'assur disappoint', 'take littl bad servic food suck', 'gave tri eat crust teeth still sore', 'complet gross', 'realli enjoy eat', 'first time go think quickli becom regular', 'server nice even though look littl overwhelm need stay profession friendli end', 'dinner companion told everyth fresh nice textur tast', 'ground right next tabl larg smear step track everywher pile green bird poop', 'furthermor even find hour oper websit', 'tri like place time think done', 'mistak', 'complaint', 'serious good pizza expert connisseur topic', 'waiter jerk', 'strike want rush', 'nicest restaur owner ever come across', 'never come', 'love biscuit', 'servic quick friendli', 'order appet took minut pizza anoth minut', 'absolutley fantast', 'huge awkward lb piec cow th gristl fat', 'definit come back', 'like steiner dark feel like bar', 'wow spici delici', 'not familiar check', 'take busi dinner dollar elsewher', 'love go back', 'anyway fs restaur wonder breakfast lunch', 'noth special', 'day week differ deal delici', 'not mention combin pear almond bacon big winner', 'not back', 'sauc tasteless', 'food delici spici enough sure ask spicier prefer way', 'ribey steak cook perfectli great mesquit flavor', 'think go back anytim soon', 'food gooodd', 'far sushi connoisseur definit tell differ good food bad food certainli bad food', 'insult', 'last time lunch bad', 'chicken wing contain driest chicken meat ever eaten', 'food good enjoy everi mouth enjoy relax venu coupl small famili group etc', 'nargil think great', 'best tater tot southwest', 'love place', 'definit not worth paid', 'vanilla ice cream creami smooth profiterol choux pastri fresh enough', 'im az time new spot', 'manag worst', 'insid realli quit nice clean', 'food outstand price reason', 'think run back carli anytim soon food', 'due fact took minut acknowledg anoth minut get food kept forget thing', 'love margarita', 'first vega buffet not disappoint', 'good though', 'one note ventil could use upgrad', 'great pork sandwich', 'wast time', 'total letdown would much rather go camelback flower shop cartel coffe', 'third chees friend burger cold', 'enjoy pizza brunch', 'steak well trim also perfectli cook', 'group claim would handl us beauti', 'love', 'ask bill leav without eat bring either', 'place jewel la vega exactli hope find nearli ten year live', 'seafood limit boil shrimp crab leg crab leg definit not tast fresh', 'select food not best', 'delici absolut back', 'small famili restaur fine dine establish', 'toro tartar cavier extraordinari like thinli slice wagyu white truffl', 'dont think back long time', 'attach ga station rare good sign', 'awesom', 'back mani time soon', 'menu much good stuff could not decid', 'wors humili worker right front bunch horribl name call', 'conclus fill meal', 'daili special alway hit group', 'tragedi struck', 'pancak also realli good pretti larg', 'first crawfish experi delici', 'monster chicken fri steak egg time favorit', 'waitress sweet funni', 'also tast mom multi grain pumpkin pancak pecan butter amaz fluffi delici', 'rather eat airlin food serious', 'cant say enough good thing place', 'ambianc incred', 'waitress manag friendli', 'would not recommend place', 'overal impress noca', 'gyro basic lettuc', 'terribl servic', 'thoroughli disappoint', 'much pasta love homemad hand made pasta thin pizza', 'give tri happi', 'far best cheesecurd ever', 'reason price also', 'everyth perfect night', 'food good typic bar food', 'drive get', 'first glanc love bakeri cafe nice ambianc clean friendli staff', 'anyway not think go back', 'point finger item menu order disappoint', 'oh thing beauti restaur', 'gone go', 'greasi unhealthi meal', 'first time might last', 'burger amaz', 'similarli deliveri man not say word apolog food minut late', 'way expens', 'sure order dessert even need pack go tiramisu cannoli die', 'first time wait next', 'bartend also nice', 'everyth good tasti', 'place two thumb way', 'best place vega breakfast check sat sun', 'love authent mexican food want whole bunch interest yet delici meat choos need tri place', 'terribl manag', 'excel new restaur experienc frenchman', 'zero star would give zero star', 'great steak great side great wine amaz dessert', 'worst martini ever', 'steak shrimp opinion best entre gc', 'opportun today sampl amaz pizza', 'wait thirti minut seat although vacant tabl folk wait', 'yellowtail carpaccio melt mouth fresh', 'tri go back even empti', 'go eat potato found stranger hair', 'spici enough perfect actual', 'last night second time dine happi decid go back', 'not even hello right', 'dessert bit strang', 'boyfriend came first time recent trip vega could not pleas qualiti food servic', 'realli recommend place go wrong donut place', 'nice ambianc', 'would recommend save room', 'guess mayb went night disgrac', 'howev recent experi particular locat not good', 'know not like restaur someth', 'avoid establish', 'think restaur suffer not tri hard enough', 'tapa dish delici', 'heart place', 'salad bland vinegrett babi green heart palm', 'two felt disgust', 'good time', 'believ place great stop huge belli hanker sushi', 'gener portion great tast', 'never go back place never ever recommend place anyon', 'server went back forth sever time not even much help', 'food delici', 'hour serious', 'consid theft', 'eew locat need complet overhaul', 'recent wit poor qualiti manag toward guest well', 'wait wait wait', 'also came back check us regularli excel servic', 'server super nice check us mani time', 'pizza tast old super chewi not good way', 'swung give tri deepli disappoint', 'servic good compani better', 'staff also friendli effici', 'servic fan quick serv nice folk', 'boy sucker dri', 'rate', 'look authent thai food go els', 'steak recommend', 'pull car wait anoth minut acknowledg', 'great food great servic clean friendli set', 'assur back', 'hate thing much cheap qualiti black oliv', 'breakfast perpar great beauti present giant slice toast lightli dust powder sugar', 'kid play area nasti', 'great place fo take eat', 'waitress friendli happi accomod vegan veggi option', 'omg felt like never eaten thai food dish', 'extrem crumbi pretti tasteless', 'pale color instead nice char flavor', 'crouton also tast homemad extra plu', 'got home see driest damn wing ever', 'regular stop trip phoenix', 'realli enjoy crema caf expand even told friend best breakfast', 'not good money', 'miss wish one philadelphia', 'got sit fairli fast end wait minut place order anoth minut food arriv', 'also best chees crisp town', 'good valu great food great servic', 'ask satisfi meal', 'food good', 'awesom', 'want leav', 'made drive way north scottsdal not one bit disappoint', 'not eat', 'owner realli realli need quit soooooo cheap let wrap freak sandwich two paper not one', 'check place coupl year ago not impress', 'chicken got definit reheat ok wedg cold soggi', 'sorri not get food anytim soon', 'absolut must visit', 'cow tongu cheek taco amaz', 'friend not like bloodi mari', 'despit hard rate busi actual rare give star', 'realli want make experi good one', 'not return', 'chicken pho tast bland', 'disappoint', 'grill chicken tender yellow saffron season', 'drive thru mean not want wait around half hour food somehow end go make us wait wait', 'pretti awesom place', 'ambienc perfect', 'best luck rude non custom servic focus new manag', 'grandmoth make roast chicken better one', 'ask multipl time wine list time ignor went hostess got one', 'staff alway super friendli help especi cool bring two small boy babi', 'four star food guy blue shirt great vibe still let us eat', 'roast beef sandwich tast realli good', 'even drastic sick', 'high qualiti chicken chicken caesar salad', 'order burger rare came done', 'promptli greet seat', 'tri go lunch madhous', 'proven dead wrong sushi bar not qualiti great servic fast food impecc', 'wait hour seat not greatest mood', 'good joint', 'macaron insan good', 'not eat', 'waiter attent friendli inform', 'mayb cold would somewhat edibl', 'place lot promis fail deliv', 'bad experi', 'mistak', 'food averag best', 'great food', 'go back anytim soon', 'disappoint order big bay plater', 'great place relax awesom burger beer', 'perfect sit famili meal get togeth friend', 'not much flavor poorli construct', 'patio seat comfort', 'fri rice dri well', 'hand favorit italian restaur', 'scream legit book somethat also pretti rare vega', 'not fun experi', 'atmospher great love duo violinist play song request', 'person love hummu pita baklava falafel baba ganoush amaz eggplant', 'conveni sinc stay mgm', 'owner super friendli staff courteou', 'great', 'eclect select', 'sweet potato tot good onion ring perfect close', 'staff attent', 'chef gener time even came around twice take pictur', 'owner use work nobu place realli similar half price', 'googl mediocr imagin smashburg pop', 'dont go', 'promis disappoint', 'sushi lover avoid place mean', 'great doubl cheeseburg', 'awesom servic food', 'fantast neighborhood gem', 'wait go back', 'plantain worst ever tast', 'great place highli recommend', 'servic slow not attent', 'gave star give star', 'staff spend time talk', 'dessert panna cotta amaz', 'good food great atmospher', 'damn good steak', 'total brunch fail', 'price reason flavor spot sauc home made slaw not drench mayo', 'decor nice piano music soundtrack pleasant', 'steak amaz rge fillet relleno best seafood plate ever', 'good food good servic', 'absolut amaz', 'probabl back honest', 'definit back', 'sergeant pepper beef sandwich auju sauc excel sandwich well', 'hawaiian breez mango magic pineappl delight smoothi tri far good', 'went lunch servic slow', 'much say place walk expect amaz quickli disappoint', 'mortifi', 'needless say never back', 'anyway food definit not fill price pay expect', 'chip came drip greas mostli not edibl', 'realli impress strip steak', 'go sinc everi meal awesom', 'server nice attent serv staff', 'cashier friendli even brought food', 'work hospit industri paradis valley refrain recommend cibo longer', 'atmospher fun', 'would not recommend other', 'servic quick even go order like like', 'mean realli get famou fish chip terribl', 'said mouth belli still quit pleas', 'not thing', 'thumb', 'read pleas go', 'love grill pizza remind legit italian pizza', 'pro larg seat area nice bar area great simpl drink menu best brick oven pizza homemad dough', 'realli nice atmospher', 'tonight elk filet special suck', 'one bite hook', 'order old classic new dish go time sore disappoint everyth', 'cute quaint simpl honest', 'chicken delici season perfect fri outsid moist chicken insid', 'food great alway compliment chef', 'special thank dylan recommend order yummi tummi', 'awesom select beer', 'great food awesom servic', 'one nice thing ad gratuiti bill sinc parti larger expect tip', 'fli appl juic fli', 'han nan chicken also tasti', 'servic thought good', 'food bare lukewarm must sit wait server bring us', 'ryan bar definit one edinburgh establish revisit', 'nicest chines restaur', 'overal like food servic', 'also serv indian naan bread hummu spici pine nut sauc world', 'probabl never come back recommend', 'friend pasta also bad bare touch', 'tri airport experi tasti food speedi friendli servic', 'love decor chines calligraphi wall paper', 'never anyth complain', 'restaur clean famili restaur feel', 'way fri', 'not sure long stood long enough begin feel awkwardli place', 'open sandwich impress not good way', 'not back', 'warm feel servic felt like guest special treat', 'extens menu provid lot option breakfast', 'alway order vegetarian menu dinner wide array option choos', 'watch price inflat portion get smaller manag attitud grow rapidli', 'wonder lil tapa ambienc made feel warm fuzzi insid', 'got enjoy seafood salad fabul vinegrett', 'wonton thin not thick chewi almost melt mouth', 'level spici perfect spice whelm soup', 'sat right time server get go fantast', 'main thing enjoy crowd older crowd around mid', 'side town definit spot hit', 'wait minut get drink longer get arepa', 'great place eat', 'jalapeno bacon soooo good', 'servic poor that nice', 'food good servic good price good', 'place not clean food oh stale', 'chicken dish ok beef like shoe leather', 'servic beyond bad', 'happi', 'tast like dirt', 'one place phoenix would defin go back', 'block amaz', 'close hous low key non fanci afford price good food', 'hot sour egg flower soup absolut star', 'sashimi poor qualiti soggi tasteless', 'great time famili dinner sunday night', 'food not tasti not say real tradit hunan style', 'bother slow servic', 'flair bartend absolut amaz', 'frozen margarita way sugari tast', 'good order twice', 'nutshel restaraunt smell like combin dirti fish market sewer', 'girlfriend veal bad', 'unfortun not good', 'pretti satifi experi', 'join club get awesom offer via email', 'perfect someon like beer ice cold case even colder', 'bland flavorless good way describ bare tepid meat', 'chain fan beat place easili', 'nacho must', 'not come back', 'mani word say place everyth pretti well', 'staff super nice quick even crazi crowd downtown juri lawyer court staff', 'great atmospher friendli fast servic', 'receiv pita huge lot meat thumb', 'food arriv meh', 'pay hot dog fri look like came kid meal wienerschnitzel not idea good meal', 'classic main lobster roll fantast', 'brother law work mall ate day guess sick night', 'good go review place twice herea tribut place tribut event held last night', 'chip salsa realli good salsa fresh', 'place great', 'mediocr food', 'get insid impress place', 'super pissd', 'servic super friendli', 'sad littl veget overcook', 'place nice surpris', 'golden crispi delici', 'high hope place sinc burger cook charcoal grill unfortun tast fell flat way flat', 'could eat bruschetta day devin', 'not singl employe came see ok even need water refil final serv us food', 'lastli mozzarella stick best thing order', 'first time ever came amaz experi still tell peopl awesom duck', 'server neglig need made us feel unwelcom would not suggest place', 'servic terribl though', 'place overpr not consist boba realli overpr', 'pack', 'love place', 'say dessert yummi', 'food terribl', 'season fruit fresh white peach pure', 'kept get wors wors offici done', 'place honestli blown', 'definit would not eat', 'not wast money', 'love put food nice plastic contain oppos cram littl paper takeout box', 'cr pe delic thin moist', 'aw servic', 'ever go', 'food qualiti horribl', 'price think place would much rather gone', 'servic fair best', 'love sushi found kabuki price hip servic', 'favor stay away dish', 'poor servic', 'one tabl thought food averag worth wait', 'best servic food ever maria server good friendli made day', 'excel', 'paid bill not tip felt server terribl job', 'lunch great experi', 'never bland food surpris consid articl read focus much spice flavor', 'food way overpr portion fuck small', 'recent tri caballero back everi week sinc', 'buck head realli expect better food', 'food came good pace', 'ate twice last visit especi enjoy salmon salad', 'back', 'could not believ dirti oyster', 'place deserv star', 'would not recommend place', 'fact go round star awesom', 'disbelief dish qualifi worst version food ever tast', 'bad day not low toler rude custom servic peopl job nice polit wash dish otherwis', 'potato great biscuit', 'probabl would not go', 'flavor perfect amount heat', 'price reason servic great', 'wife hate meal coconut shrimp friend realli not enjoy meal either', 'fella got huevo ranchero look appeal', 'went happi hour great list wine', 'may say buffet pricey think get pay place get quit lot', 'probabl come back', 'worst food servic', 'place pretti good nice littl vibe restaur', 'talk great custom servic cours back', 'hot dish not hot cold dish close room temp watch staff prepar food bare hand glove everyth deep fri oil', 'love fri bean', 'alway pleasur deal', 'plethora salad sandwich everyth tri get seal approv', 'place awesom want someth light healthi summer', 'sushi strip place go', 'servic great even manag came help tabl', 'feel dine room colleg cook cours high class dine servic slow best', 'start review two star edit give one', 'worst sushi ever eat besid costco', 'excel restaur highlight great servic uniqu menu beauti set', 'boyfriend sat bar complet delight experi', 'weird vibe owner', 'hardli meat', 'better bagel groceri store', 'go place gyro', 'love owner chef one authent japanes cool dude', 'burger good pizza use amaz doughi flavorless', 'found six inch long piec wire salsa', 'servic terribl food mediocr', 'defin enjoy', 'order albondiga soup warm tast like tomato soup frozen meatbal', 'three differ occas ask well done medium well three time got bloodiest piec meat plate', 'two bite refus eat anymor', 'servic extrem slow', 'minut wait got tabl', 'serious killer hot chai latt', 'allergi warn menu waitress absolut clue meal not contain peanut', 'boyfriend tri mediterranean chicken salad fell love', 'rotat beer tap also highlight place', 'price bit concern mellow mushroom', 'worst thai ever', 'stay vega must get breakfast least', 'want first say server great perfect servic', 'pizza select good', 'strawberri tea good', 'highli unprofession rude loyal patron', 'overal great experi', 'spend money elsewher', 'regular toast bread equal satisfi occasion pat butter mmmm', 'buffet bellagio far anticip', 'drink weak peopl', 'order not correct', 'also feel like chip bought not made hous', 'disappoint dinner went elsewher dessert', 'chip sal amaz', 'return', 'new fav vega buffet spot', 'serious cannot believ owner mani unexperienc employe run around like chicken head cut', 'sad', 'felt insult disrespect could talk judg anoth human like', 'call steakhous properli cook steak understand', 'not impress concept food', 'thing crazi guacamol like pur ed', 'realli noth postino hope experi better', 'got food poison buffet', 'brought fresh batch fri think yay someth warm', 'hilari yummi christma eve dinner rememb biggest fail entir trip us', 'needless say go back anytim soon', 'place disgust', 'everi time eat see care teamwork profession degre', 'ri style calamari joke', 'howev much garlic fondu bare edibl', 'could bare stomach meal complain busi lunch', 'bad lost heart finish', 'also took forev bring us check ask', 'one make scene restaur get definit lost love one', 'disappoint experi', 'food par denni say not good', 'want wait mediocr food downright terribl servic place', 'waaaaaayyyyyyyyyi rate say', 'go back', 'place fairli clean food simpli worth', 'place lack style', 'sangria half glass wine full ridicul', 'bother come', 'meat pretti dri slice brisket pull pork', 'build seem pretti neat bathroom pretti trippi eat', 'equal aw', 'probabl not hurri go back', 'slow seat even reserv', 'not good stretch imagin', 'cashew cream sauc bland veget undercook', 'chipolt ranch dip saus tasteless seem thin water heat', 'bit sweet not realli spici enough lack flavor', 'disappoint', 'place horribl way overpr', 'mayb vegetarian fare twice thought averag best', 'busi know', 'tabl outsid also dirti lot time worker not alway friendli help menu', 'ambianc not feel like buffet set douchey indoor garden tea biscuit', 'con spotti servic', 'fri not hot neither burger', 'came back cold', 'food came disappoint ensu', 'real disappoint waiter', 'husband said rude not even apolog bad food anyth', 'reason eat would fill night bing drink get carb stomach', 'insult profound deuchebaggeri go outsid smoke break serv solidifi', 'someon order two taco think may part custom servic ask combo ala cart', 'quit disappoint although blame need place door', 'rave review wait eat disappoint', 'del taco pretti nasti avoid possibl', 'not hard make decent hamburg', 'like', 'hell go back', 'gotten much better servic pizza place next door servic receiv restaur', 'know big deal place back ya', 'immedi said want talk manag not want talk guy shot firebal behind bar', 'ambianc much better', 'unfortun set us disapppoint entre', 'food good', 'server suck wait correct server heimer suck', 'happen next pretti put', 'bad caus know famili own realli want like place', 'overpr get', 'vomit bathroom mid lunch', 'kept look time soon becom minut yet still food', 'place eat circumst would ever return top list', 'start tuna sashimi brownish color obvious fresh', 'food averag', 'sure beat nacho movi would expect littl bit come restaur', 'ha long bay bit flop', 'problem charg sandwich bigger subway sub offer better amount veget', 'shrimp unwrap live mile brushfir liter ice cold', 'lack flavor seem undercook dri', 'realli impress place close', 'would avoid place stay mirag', 'refri bean came meal dri crusti food bland', 'spend money time place els', 'ladi tabl next us found live green caterpillar salad', 'present food aw', 'tell disappoint', 'think food flavor textur lack', 'appetit instantli gone', 'overal not impress would not go back', 'whole experi underwhelm think go ninja sushi next time', 'wast enough life pour salt wound draw time took bring check']\n"
          ]
        }
      ],
      "source": [
        "print(corpus)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "CLqmAkANCp1-"
      },
      "source": [
        "## Creating the Bag of Words model"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 18,
      "metadata": {},
      "outputs": [],
      "source": [
        "from sklearn.feature_extraction.text import CountVectorizer\n",
        "cv = CountVectorizer(max_features=1500)\n",
        "X = cv.fit_transform(corpus).toarray()\n",
        "y = data.iloc[:,-1].values"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "First do not provide any arguments to CountVectorizer and run to form X and then calculate its size by printing len(X[0]) and here it is 1566.\n",
        "\n",
        "Now we can further reduce the size of the bag of words by removing some words such as steve, bank, etc which do not help in predictions. We can do this by removing the words whose frequency is greater than a set limit\n",
        "\n",
        "Now add an argument to CountVectorizer as max_features = 1500 to only get the words whose position when ordered in decreasing order of frequency is in the range 1 - 1500. So it removes the 66 least repeating words"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 19,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "1500\n"
          ]
        }
      ],
      "source": [
        "print(len(X[0]))"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "DH_VjgPzC2cd"
      },
      "source": [
        "## Splitting the dataset into the Training set and Test set"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 20,
      "metadata": {},
      "outputs": [],
      "source": [
        "from sklearn.model_selection import train_test_split\n",
        "X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=0, test_size = 0.2)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "VkIq23vEDIPt"
      },
      "source": [
        "## Training the Classification Model on the Training set"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 21,
      "metadata": {},
      "outputs": [
        {
          "data": {
            "text/html": [
              "<style>#sk-container-id-2 {\n",
              "  /* Definition of color scheme common for light and dark mode */\n",
              "  --sklearn-color-text: black;\n",
              "  --sklearn-color-line: gray;\n",
              "  /* Definition of color scheme for unfitted estimators */\n",
              "  --sklearn-color-unfitted-level-0: #fff5e6;\n",
              "  --sklearn-color-unfitted-level-1: #f6e4d2;\n",
              "  --sklearn-color-unfitted-level-2: #ffe0b3;\n",
              "  --sklearn-color-unfitted-level-3: chocolate;\n",
              "  /* Definition of color scheme for fitted estimators */\n",
              "  --sklearn-color-fitted-level-0: #f0f8ff;\n",
              "  --sklearn-color-fitted-level-1: #d4ebff;\n",
              "  --sklearn-color-fitted-level-2: #b3dbfd;\n",
              "  --sklearn-color-fitted-level-3: cornflowerblue;\n",
              "\n",
              "  /* Specific color for light theme */\n",
              "  --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
              "  --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, white)));\n",
              "  --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, black)));\n",
              "  --sklearn-color-icon: #696969;\n",
              "\n",
              "  @media (prefers-color-scheme: dark) {\n",
              "    /* Redefinition of color scheme for dark theme */\n",
              "    --sklearn-color-text-on-default-background: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
              "    --sklearn-color-background: var(--sg-background-color, var(--theme-background, var(--jp-layout-color0, #111)));\n",
              "    --sklearn-color-border-box: var(--sg-text-color, var(--theme-code-foreground, var(--jp-content-font-color1, white)));\n",
              "    --sklearn-color-icon: #878787;\n",
              "  }\n",
              "}\n",
              "\n",
              "#sk-container-id-2 {\n",
              "  color: var(--sklearn-color-text);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 pre {\n",
              "  padding: 0;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 input.sk-hidden--visually {\n",
              "  border: 0;\n",
              "  clip: rect(1px 1px 1px 1px);\n",
              "  clip: rect(1px, 1px, 1px, 1px);\n",
              "  height: 1px;\n",
              "  margin: -1px;\n",
              "  overflow: hidden;\n",
              "  padding: 0;\n",
              "  position: absolute;\n",
              "  width: 1px;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-dashed-wrapped {\n",
              "  border: 1px dashed var(--sklearn-color-line);\n",
              "  margin: 0 0.4em 0.5em 0.4em;\n",
              "  box-sizing: border-box;\n",
              "  padding-bottom: 0.4em;\n",
              "  background-color: var(--sklearn-color-background);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-container {\n",
              "  /* jupyter's normalize.less sets [hidden] { display: none; }\n",
              "     but bootstrap.min.css set [hidden] { display: none !important; }\n",
              "     so we also need the !important here to be able to override the\n",
              "     default hidden behavior on the sphinx rendered scikit-learn.org.\n",
              "     See: https://github.com/scikit-learn/scikit-learn/issues/21755 */\n",
              "  display: inline-block !important;\n",
              "  position: relative;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-text-repr-fallback {\n",
              "  display: none;\n",
              "}\n",
              "\n",
              "div.sk-parallel-item,\n",
              "div.sk-serial,\n",
              "div.sk-item {\n",
              "  /* draw centered vertical line to link estimators */\n",
              "  background-image: linear-gradient(var(--sklearn-color-text-on-default-background), var(--sklearn-color-text-on-default-background));\n",
              "  background-size: 2px 100%;\n",
              "  background-repeat: no-repeat;\n",
              "  background-position: center center;\n",
              "}\n",
              "\n",
              "/* Parallel-specific style estimator block */\n",
              "\n",
              "#sk-container-id-2 div.sk-parallel-item::after {\n",
              "  content: \"\";\n",
              "  width: 100%;\n",
              "  border-bottom: 2px solid var(--sklearn-color-text-on-default-background);\n",
              "  flex-grow: 1;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-parallel {\n",
              "  display: flex;\n",
              "  align-items: stretch;\n",
              "  justify-content: center;\n",
              "  background-color: var(--sklearn-color-background);\n",
              "  position: relative;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-parallel-item {\n",
              "  display: flex;\n",
              "  flex-direction: column;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-parallel-item:first-child::after {\n",
              "  align-self: flex-end;\n",
              "  width: 50%;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-parallel-item:last-child::after {\n",
              "  align-self: flex-start;\n",
              "  width: 50%;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-parallel-item:only-child::after {\n",
              "  width: 0;\n",
              "}\n",
              "\n",
              "/* Serial-specific style estimator block */\n",
              "\n",
              "#sk-container-id-2 div.sk-serial {\n",
              "  display: flex;\n",
              "  flex-direction: column;\n",
              "  align-items: center;\n",
              "  background-color: var(--sklearn-color-background);\n",
              "  padding-right: 1em;\n",
              "  padding-left: 1em;\n",
              "}\n",
              "\n",
              "\n",
              "/* Toggleable style: style used for estimator/Pipeline/ColumnTransformer box that is\n",
              "clickable and can be expanded/collapsed.\n",
              "- Pipeline and ColumnTransformer use this feature and define the default style\n",
              "- Estimators will overwrite some part of the style using the sk-estimator class\n",
              "*/\n",
              "\n",
              "/* Pipeline and ColumnTransformer style (default) */\n",
              "\n",
              "#sk-container-id-2 div.sk-toggleable {\n",
              "  /* Default theme specific background. It is overwritten whether we have a\n",
              "  specific estimator or a Pipeline/ColumnTransformer */\n",
              "  background-color: var(--sklearn-color-background);\n",
              "}\n",
              "\n",
              "/* Toggleable label */\n",
              "#sk-container-id-2 label.sk-toggleable__label {\n",
              "  cursor: pointer;\n",
              "  display: block;\n",
              "  width: 100%;\n",
              "  margin-bottom: 0;\n",
              "  padding: 0.5em;\n",
              "  box-sizing: border-box;\n",
              "  text-align: center;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 label.sk-toggleable__label-arrow:before {\n",
              "  /* Arrow on the left of the label */\n",
              "  content: \"▸\";\n",
              "  float: left;\n",
              "  margin-right: 0.25em;\n",
              "  color: var(--sklearn-color-icon);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 label.sk-toggleable__label-arrow:hover:before {\n",
              "  color: var(--sklearn-color-text);\n",
              "}\n",
              "\n",
              "/* Toggleable content - dropdown */\n",
              "\n",
              "#sk-container-id-2 div.sk-toggleable__content {\n",
              "  max-height: 0;\n",
              "  max-width: 0;\n",
              "  overflow: hidden;\n",
              "  text-align: left;\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-0);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-toggleable__content.fitted {\n",
              "  /* fitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-0);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-toggleable__content pre {\n",
              "  margin: 0.2em;\n",
              "  border-radius: 0.25em;\n",
              "  color: var(--sklearn-color-text);\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-0);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-toggleable__content.fitted pre {\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-0);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 input.sk-toggleable_control:checked~div.sk-toggleable_content {\n",
              "  /* Expand drop-down */\n",
              "  max-height: 200px;\n",
              "  max-width: 100%;\n",
              "  overflow: auto;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 input.sk-toggleable_control:checked~label.sk-toggleable_label-arrow:before {\n",
              "  content: \"▾\";\n",
              "}\n",
              "\n",
              "/* Pipeline/ColumnTransformer-specific style */\n",
              "\n",
              "#sk-container-id-2 div.sk-label input.sk-toggleable_control:checked~label.sk-toggleable_label {\n",
              "  color: var(--sklearn-color-text);\n",
              "  background-color: var(--sklearn-color-unfitted-level-2);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-label.fitted input.sk-toggleable_control:checked~label.sk-toggleable_label {\n",
              "  background-color: var(--sklearn-color-fitted-level-2);\n",
              "}\n",
              "\n",
              "/* Estimator-specific style */\n",
              "\n",
              "/* Colorize estimator box */\n",
              "#sk-container-id-2 div.sk-estimator input.sk-toggleable_control:checked~label.sk-toggleable_label {\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-2);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-estimator.fitted input.sk-toggleable_control:checked~label.sk-toggleable_label {\n",
              "  /* fitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-2);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-label label.sk-toggleable__label,\n",
              "#sk-container-id-2 div.sk-label label {\n",
              "  /* The background is the default theme color */\n",
              "  color: var(--sklearn-color-text-on-default-background);\n",
              "}\n",
              "\n",
              "/* On hover, darken the color of the background */\n",
              "#sk-container-id-2 div.sk-label:hover label.sk-toggleable__label {\n",
              "  color: var(--sklearn-color-text);\n",
              "  background-color: var(--sklearn-color-unfitted-level-2);\n",
              "}\n",
              "\n",
              "/* Label box, darken color on hover, fitted */\n",
              "#sk-container-id-2 div.sk-label.fitted:hover label.sk-toggleable__label.fitted {\n",
              "  color: var(--sklearn-color-text);\n",
              "  background-color: var(--sklearn-color-fitted-level-2);\n",
              "}\n",
              "\n",
              "/* Estimator label */\n",
              "\n",
              "#sk-container-id-2 div.sk-label label {\n",
              "  font-family: monospace;\n",
              "  font-weight: bold;\n",
              "  display: inline-block;\n",
              "  line-height: 1.2em;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-label-container {\n",
              "  text-align: center;\n",
              "}\n",
              "\n",
              "/* Estimator-specific */\n",
              "#sk-container-id-2 div.sk-estimator {\n",
              "  font-family: monospace;\n",
              "  border: 1px dotted var(--sklearn-color-border-box);\n",
              "  border-radius: 0.25em;\n",
              "  box-sizing: border-box;\n",
              "  margin-bottom: 0.5em;\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-0);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-estimator.fitted {\n",
              "  /* fitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-0);\n",
              "}\n",
              "\n",
              "/* on hover */\n",
              "#sk-container-id-2 div.sk-estimator:hover {\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-2);\n",
              "}\n",
              "\n",
              "#sk-container-id-2 div.sk-estimator.fitted:hover {\n",
              "  /* fitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-2);\n",
              "}\n",
              "\n",
              "/* Specification for estimator info (e.g. \"i\" and \"?\") */\n",
              "\n",
              "/* Common style for \"i\" and \"?\" */\n",
              "\n",
              ".sk-estimator-doc-link,\n",
              "a:link.sk-estimator-doc-link,\n",
              "a:visited.sk-estimator-doc-link {\n",
              "  float: right;\n",
              "  font-size: smaller;\n",
              "  line-height: 1em;\n",
              "  font-family: monospace;\n",
              "  background-color: var(--sklearn-color-background);\n",
              "  border-radius: 1em;\n",
              "  height: 1em;\n",
              "  width: 1em;\n",
              "  text-decoration: none !important;\n",
              "  margin-left: 1ex;\n",
              "  /* unfitted */\n",
              "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
              "  color: var(--sklearn-color-unfitted-level-1);\n",
              "}\n",
              "\n",
              ".sk-estimator-doc-link.fitted,\n",
              "a:link.sk-estimator-doc-link.fitted,\n",
              "a:visited.sk-estimator-doc-link.fitted {\n",
              "  /* fitted */\n",
              "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
              "  color: var(--sklearn-color-fitted-level-1);\n",
              "}\n",
              "\n",
              "/* On hover */\n",
              "div.sk-estimator:hover .sk-estimator-doc-link:hover,\n",
              ".sk-estimator-doc-link:hover,\n",
              "div.sk-label-container:hover .sk-estimator-doc-link:hover,\n",
              ".sk-estimator-doc-link:hover {\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-3);\n",
              "  color: var(--sklearn-color-background);\n",
              "  text-decoration: none;\n",
              "}\n",
              "\n",
              "div.sk-estimator.fitted:hover .sk-estimator-doc-link.fitted:hover,\n",
              ".sk-estimator-doc-link.fitted:hover,\n",
              "div.sk-label-container:hover .sk-estimator-doc-link.fitted:hover,\n",
              ".sk-estimator-doc-link.fitted:hover {\n",
              "  /* fitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-3);\n",
              "  color: var(--sklearn-color-background);\n",
              "  text-decoration: none;\n",
              "}\n",
              "\n",
              "/* Span, style for the box shown on hovering the info icon */\n",
              ".sk-estimator-doc-link span {\n",
              "  display: none;\n",
              "  z-index: 9999;\n",
              "  position: relative;\n",
              "  font-weight: normal;\n",
              "  right: .2ex;\n",
              "  padding: .5ex;\n",
              "  margin: .5ex;\n",
              "  width: min-content;\n",
              "  min-width: 20ex;\n",
              "  max-width: 50ex;\n",
              "  color: var(--sklearn-color-text);\n",
              "  box-shadow: 2pt 2pt 4pt #999;\n",
              "  /* unfitted */\n",
              "  background: var(--sklearn-color-unfitted-level-0);\n",
              "  border: .5pt solid var(--sklearn-color-unfitted-level-3);\n",
              "}\n",
              "\n",
              ".sk-estimator-doc-link.fitted span {\n",
              "  /* fitted */\n",
              "  background: var(--sklearn-color-fitted-level-0);\n",
              "  border: var(--sklearn-color-fitted-level-3);\n",
              "}\n",
              "\n",
              ".sk-estimator-doc-link:hover span {\n",
              "  display: block;\n",
              "}\n",
              "\n",
              "/* \"?\"-specific style due to the <a> HTML tag */\n",
              "\n",
              "#sk-container-id-2 a.estimator_doc_link {\n",
              "  float: right;\n",
              "  font-size: 1rem;\n",
              "  line-height: 1em;\n",
              "  font-family: monospace;\n",
              "  background-color: var(--sklearn-color-background);\n",
              "  border-radius: 1rem;\n",
              "  height: 1rem;\n",
              "  width: 1rem;\n",
              "  text-decoration: none;\n",
              "  /* unfitted */\n",
              "  color: var(--sklearn-color-unfitted-level-1);\n",
              "  border: var(--sklearn-color-unfitted-level-1) 1pt solid;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 a.estimator_doc_link.fitted {\n",
              "  /* fitted */\n",
              "  border: var(--sklearn-color-fitted-level-1) 1pt solid;\n",
              "  color: var(--sklearn-color-fitted-level-1);\n",
              "}\n",
              "\n",
              "/* On hover */\n",
              "#sk-container-id-2 a.estimator_doc_link:hover {\n",
              "  /* unfitted */\n",
              "  background-color: var(--sklearn-color-unfitted-level-3);\n",
              "  color: var(--sklearn-color-background);\n",
              "  text-decoration: none;\n",
              "}\n",
              "\n",
              "#sk-container-id-2 a.estimator_doc_link.fitted:hover {\n",
              "  /* fitted */\n",
              "  background-color: var(--sklearn-color-fitted-level-3);\n",
              "}\n",
              "</style><div id=\"sk-container-id-2\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>SVC(random_state=0)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator fitted sk-toggleable\"><input class=\"sk-toggleable_control sk-hidden--visually\" id=\"sk-estimator-id-2\" type=\"checkbox\" checked><label for=\"sk-estimator-id-2\" class=\"sk-toggleablelabel fitted sk-toggleablelabel-arrow fitted\">&nbsp;&nbsp;SVC<a class=\"sk-estimator-doc-link fitted\" rel=\"noreferrer\" target=\"_blank\" href=\"https://scikit-learn.org/1.4/modules/generated/sklearn.svm.SVC.html\">?<span>Documentation for SVC</span></a><span class=\"sk-estimator-doc-link fitted\">i<span>Fitted</span></span></label><div class=\"sk-toggleable_content fitted\"><pre>SVC(random_state=0)</pre></div> </div></div></div></div>"
            ],
            "text/plain": [
              "SVC(random_state=0)"
            ]
          },
          "execution_count": 21,
          "metadata": {},
          "output_type": "execute_result"
        }
      ],
      "source": [
        "from sklearn.svm import SVC\n",
        "classifier = SVC(kernel = 'rbf',random_state = 0)\n",
        "classifier.fit(X_train, y_train)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "1JaRM7zXDWUy"
      },
      "source": [
        "## Predicting the Test set results"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 22,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
            "text": [
            "[0 0 0 0 0 0 1 0 0 1 1 1 1 1 1 1 0 0 0 1 0 0 1 0 0 1 0 1 1 0 0 0 0 0 1 0 0\n",
            " 0 0 1 1 0 0 0 0 0 1 1 0 0 1 0 1 1 0 0 0 0 0 1 0 0 0 1 0 0 1 0 0 0 1 1 1 0\n",
            " 0 0 0 1 0 1 0 1 1 0 1 1 0 0 1 0 0 1 0 0 0 0 1 0 0 0 0 1 1 1 0 0 1 1 0 0 0\n",
            " 1 0 1 0 0 1 1 1 1 0 0 1 0 0 0 0 0 0 0 0 1 0 0 1 1 1 1 1 0 1 1 1 0 0 0 0 0\n",
            " 0 0 0 0 1 1 0 0 1 0 1 0 0 0 1 1 1 0 0 0 0 0 0 1 1 0 0 0 0 1 0 1 1 0 0 0 0\n",
            " 0 0 1 0 1 1 0 0 0 1 0 1 1 0 0]\n"
          ]
        }
      ],
      "source": [
        "y_pred = classifier.predict(X_test)\n",
        "print(y_pred)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id":" xoMltea5Dir1"
        },
      "source": [
        "## Making the Confusion Matrix"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 23,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "[[89  8]\n",
            " [36 67]]\n",
            "0.78\n"
          ]
        }
      ],
      "source": [
        "from sklearn.metrics import confusion_matrix,accuracy_score\n",
        "cm = confusion_matrix(y_test,y_pred)\n",
        "acc = accuracy_score(y_test,y_pred)\n",
        "print(cm)\n",
        "print(acc)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "## Predicting if a single review is positive or negative"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### Positive review"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 24,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "[1]\n"
          ]
        }
      ],
      "source": [
        "new_review = 'I love this restaurant so much'\n",
        "new_review = re.sub('[^a-zA-Z]', ' ', new_review)\n",
        "new_review = new_review.lower()\n",
        "new_review = new_review.split()\n",
        "ps = PorterStemmer()\n",
        "all_stopwords = stopwords.words('english')\n",
        "all_stopwords.remove('not')\n",
        "new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]\n",
        "new_review = ' '.join(new_review)\n",
        "new_corpus = [new_review]\n",
        "new_X_test = cv.transform(new_corpus).toarray()\n",
        "new_y_pred = classifier.predict(new_X_test)\n",
        "print(new_y_pred)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "Correct prediction"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "### Negative review"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 25,
      "metadata": {},
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "[0]\n"
          ]
        }
      ],
      "source": [
        "new_review = 'I hate this restaurant so much'\n",
        "new_review = re.sub('[^a-zA-Z]', ' ', new_review)\n",
        "new_review = new_review.lower()\n",
        "new_review = new_review.split()\n",
        "ps = PorterStemmer()\n",
        "all_stopwords = stopwords.words('english')\n",
        "all_stopwords.remove('not')\n",
        "new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]\n",
        "new_review = ' '.join(new_review)\n",
        "new_corpus = [new_review]\n",
        "new_X_test = cv.transform(new_corpus).toarray()\n",
        "new_y_pred = classifier.predict(new_X_test)\n",
        "print(new_y_pred)"
      ]
    },
      {
      "cell_type": "markdown",
      "metadata": {},
      "source": [
        "Correct prediction"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "collapsed_sections": [],
      "name": "natural_language_processing.ipynb",
      "provenance": [],
      "toc_visible":True
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "codemirror_mode": {
        "name": "ipython",
        "version": 3
      },
      "file_extension": ".py",
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "pygments_lexer": "ipython3",
      "version": "3.12.3",

    }
  },
  "nbformat": 4,
  "nbformat_minor": 0,
  
}
