# 易經圖片生成指南（Nano Banana）

## 專案視覺定位
易經不同於塔羅牌的具象敘事，其核心在於「陰陽符號」的抽象組合與「天地人」的氣場流動。
本專案的視覺風格定位為：**「現代東方禪意 (Modern Oriental Zen)」**。
-   **關鍵字**：簡約、水墨、氣場、光影、符號化、玄武岩、竹、雲霧。
-   **色調**：黑、白、灰 為主，輔以極少量的古銅金（代表陽）或深藏青（代表陰）。

## 第一部分：UI 基礎元件 - 標準卦象 (Symbolic Hexagrams)

這部分**不需要 AI 生成**，應在 UI 層面（Streamlit）使用程式碼動態繪製，以確保符號的絕對準確性。

### 1. 爻的定義 (Line Definitions)
| 爻象 | 名稱 | 程式碼表示 (邏輯) | UI 繪製規範 |
| :--- | :--- | :--- | :--- |
| **——** | 陽爻 (Yang) | `1` | 一條連續的黑色粗橫線。 |
| **-- --** | 陰爻 (Yin) | `0` | 兩條中間斷開的黑色粗橫線，斷開處約佔全長的 1/5。 |

### 2. 卦象繪製規範
-   **組合**：由下而上，將 6 個爻垂直堆疊。
-   **間距**：爻與爻之間的垂直間距應均勻，約等於一條陽爻的厚度。
-   **呈現**：
    -   **本卦**：使用標準黑線。
    -   **變卦**：與本卦並列，高亮標示出**發生變動的爻**（例如：動爻使用古銅金色，靜爻保留黑色）。

---

## 第二部分：AI 生成意境圖 (Atmospheric Images)

這部分用於為 64 卦生成具有視覺衝擊力的背景圖或代表圖，存放在 `assets/images/hexagrams/{id}.png`。

### 1. 通用 Prompt 結構 (Universal Prompt Structure)

為了保持風格統一，所有卦象的 Prompt 都應包含以下核心描述：

> **[Hexagram Concept]**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

### 2. 八大基礎卦（三爻卦）的視覺元素 (Trigram Visual Elements)

64 卦由以下八個基礎元素兩兩組合而成。在生成複合卦象圖時，應融合這兩個元素的特徵：

| 元素 | 卦名 | Prompt 關鍵字 (Elements) | 視覺呈現建議 |
| :--- | :--- | :--- | :--- |
| **天** | 乾 (Qian) | Sky, heaven, vast cosmos, endless swirling clouds, divine light. | 宏大、蒼穹、向上流動的氣。 |
| **地** | 坤 (Kun) | Earth, fertile soil, deep canyon, mossy stone, roots. | 穩重、包容、向下紮根的質感。 |
| **水** | 坎 (Kan) | Water, abyss, deep ocean trench, rapid river, moonlight on waves. | 深邃、流動、險陷的光影。 |
| **火** | 離 (Li) | Fire, sun, burning ember, aurora, radiant heat, dancing flame. | 光明、熱烈、向外擴散的能量。 |
| **雷** | 震 (Zhen) | Thunder, lightning bolt, electric discharge, cracking rock. | 瞬間的爆發力、震動感。 |
| **風** | 巽 (Xun) | Wind, breeze, bamboo forest sways, tornado, dandelion seeds. | 輕盈、無孔不入、流動的線條。 |
| **山** | 艮 (Gen) | Mountain, peak, giant basalt columns, serenity, timeless rock. | 靜止、高聳、阻擋的體量感。 |
| **澤** | 兌 (Dui) | Lake, marshland, still water reflection, lotus flower, reeds. | 愉悅、平靜、倒影的美感。 |

### 3. 具体卦象 Prompt 生成範例

我們取你 JSON 資料庫中的前四卦為例：

#### 卦 1：乾為天 (Id: 1)
* **概念**：天 + 天（絕對的純陽、剛健）。
* **Prompt**：
    > **Vast, swirling cosmos with nine divine dragons flying through endless white clouds**, ethereal light rays pouring from above, highly detailed oriental ink style, Zen atmosphere, minimalism, black and white with subtle metallic gold accents, 8k. --ar 3:4

#### 卦 2：坤為地 (Id: 2)
* **概念**：地 + 地（絕對的純陰、柔順）。
* **Prompt**：
    > **Deep, ancient canyon with roots gnarled through fertile black soil, countless stones shaped by time**, mist settled at the bottom, surreal oriental ink style, Zen atmosphere, minimalism, monochromatic grey and black, 8k. --ar 3:4

#### 卦 3：水雷屯 (Id: 3)
* **概念**：水（困難）+ 雷（動）（草創艱難，但有生機）。
* **Prompt**：
    > **A violent thunderstorm over a deep, dark abyss. A small, resilient green sprout is cracking open a massive basalt rock under a flash of lightning**, heavy rain, mysterious mist, highly detailed oriental ink style, Zen atmosphere, contrast of dark waves and bright electric spark, 8k. --ar 3:4

#### 卦 4：山水蒙 (Id: 4)
* **概念**：山 + 水（山下有險，蒙昧不明）。
* **Prompt**：
    > **A majestic, timeless mountain peak shrouded in dense, low-hanging clouds and thick fog**, a dark, winding river flows at its base, mysterious and hazy atmosphere, soft moonlight filtering through, surreal oriental ink style, Zen minimalism, monochromatic, 8k. --ar 3:4

#### 卦 5：水天需 (Id: 5)
* **概念**：水（坎） + 天（乾）（雲氣上集於天，待時而降）。代表「等待、醞釀」。
* **Prompt**：
    > **Heavy, dark rain clouds gathering in a vast, bright sky above a calm, dry landscape, a sense of quiet anticipation and stillness**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 6：天水訟 (Id: 6)
* **概念**：天（乾） + 水（坎）（天道向上，水性向下，背道而馳）。代表「衝突、分歧」。
* **Prompt**：
    > **A stark, dramatic division between an ethereal, glowing sky soaring upwards and a deep, turbulent whirlpool churning below, conflicting energies pulling apart**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 7：地水師 (Id: 7)
* **概念**：地（坤） + 水（坎）（地下有水，深藏不露）。代表「軍隊、潛藏的規律與力量」。
* **Prompt**：
    > **A powerful, rapid underground river flowing fiercely beneath solid, ancient earth and massive rock formations, immense latent energy hidden in the dark**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 8：水地比 (Id: 8)
* **概念**：水（坎） + 地（坤）（水依附於地，交融無間）。代表「親密、和諧、輔助」。
* **Prompt**：
    > **A perfectly calm, mirror-like lake seamlessly merging with a vast, flat plain, gentle ripples touching the muddy shore in perfect harmony**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 9：風天小畜 (Id: 9)
* **概念**：風（巽） + 天（乾）（風行天上，密雲不雨）。代表「微小的積蓄、溫和的牽制」。
* **Prompt**：
    > **Gentle, sweeping winds shaping high, wispy clouds across an endless sky, a subtle tension of impending weather but no rain**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 10：天澤履 (Id: 10)
* **概念**：天（乾） + 澤（兌）（天上澤下，伴君如伴虎）。代表「小心履冰、謹慎前行」。
* **Prompt**：
    > **Subtle footprints on a precarious rocky edge overlooking a deep, crystal-clear lake reflecting the immense sky, a sense of walking on thin ice, tension and beauty**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 11：地天泰 (Id: 11)
* **概念**：地（坤） + 天（乾）（天地交泰，陰陽融合）。代表「通達、和平、最完美的平衡」。
* **Prompt**：
    > **A surreal, harmonious landscape where floating islands of fertile earth gracefully merge with glowing celestial clouds, perfect balance and peace**, warm ethereal lighting, surreal oriental ink painting style, Zen atmosphere, minimalism, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 12：天地否 (Id: 12)
* **概念**：天（乾） + 地（坤）（天高高在上，地卑微在下，互不交集）。代表「閉塞、停滯、溝通中斷」。
* **Prompt**：
    > **A desolate, cracked earth utterly separated from a distant, cold sky by a vast, empty void, complete disconnection and heavy stillness**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 13：天火同人 (Id: 13)
* **概念**：天（乾） + 火（離）（火光沖天，與天同輝）。代表「志同道合、集結眾人」。
* **Prompt**：
    > **A solitary, bright bonfire on an open, vast plain, its glowing embers and flames rising upward to seamlessly merge with the shining stars in the night sky, a sense of unity and fellowship**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 14：火天大有 (Id: 14)
* **概念**：火（離） + 天（乾）（火在天上，如同太陽普照萬物）。代表「大豐收、擁有極大財富與能量」。
* **Prompt**：
    > **A radiant, divine golden sun glowing intensely high in the sky, illuminating a vast, majestic landscape of rolling hills and endless clouds, casting striking shadows and bringing immense abundance**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 15：地山謙 (Id: 15)
* **概念**：地（坤） + 山（艮）（高山隱藏於平地之下）。代表「謙虛、內斂、不露鋒芒」。
* **Prompt**：
    > **A massive, majestic mountain peak bowing downwards, partially submerged and gently hidden beneath the endless, flat surface of the earth, profound humility and quiet strength**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 16：雷地豫 (Id: 16)
* **概念**：雷（震） + 地（坤）（春雷動於地下，萬物復甦）。代表「歡樂、熱情、順應時機」。
* **Prompt**：
    > **A powerful burst of golden lightning cracking upward from deep within the fertile, dark soil, awakening dormant ancient roots, dynamic energy of early spring breaking through the silent ground**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 17：澤雷隨 (Id: 17)
* **概念**：澤（兌） + 雷（震）（雷隱藏在秋天的沼澤之下，進入休眠）。代表「順應、跟隨、休息」。
* **Prompt**：
    > **A completely calm, mysterious dark lake surface with subtle, glowing electrical currents of thunder silently illuminating the deep water from below, resting energy and profound adaptation**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 18：山風蠱 (Id: 18)
* **概念**：山（艮） + 風（巽）（風在山下吹拂，空氣不流通導致腐敗）。代表「腐朽、需要整頓與重生」。
* **Prompt**：
    > **A stagnant, ancient valley at the foot of a towering mountain, twisted, dying branches being slowly blown away by a low, cleansing glowing breeze, the process of decay turning into renewal**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 19：地澤臨 (Id: 19)
* **概念**：地（坤） + 澤（兌）（大地高臨於湖澤之上）。代表「居高臨下、視察、溫和的統治」。
* **Prompt**：
    > **A high, solid cliff of rich earth gently curving over and reflecting upon a vast, pristine lake below, a sense of protective and benevolent oversight**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 20：風地觀 (Id: 20)
* **概念**：風（巽） + 地（坤）（風吹拂過大地，無所不至）。代表「觀察、省視、展現給眾人看」。
* **Prompt**：
    > **A gentle, sweeping wind blowing through a sparse, elegant bamboo grove on a high hill, overlooking the vast, silent plains below, profound contemplation and a high vantage point**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4


#### 卦 21：火雷噬嗑 (Id: 21)
* **概念**：火（離） + 雷（震）（咬碎障礙，雷電交加）。代表「排除萬難、執行刑罰與紀律」。
* **Prompt**：
    > **A powerful jaw-like dark mountain formation being fiercely struck by golden lightning, bright flames erupting from the cracked basalt rocks, intense energy breaking through heavy obstacles**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 22：山火賁 (Id: 22)
* **概念**：山（艮） + 火（離）（山下有火，火光照耀山壁）。代表「裝飾、晚霞、表面的美麗與優雅」。
* **Prompt**：
    > **A serene, towering dark mountain gracefully illuminated from below by a gentle, glowing golden fire, beautiful warm light blending with stark ink lines, elegant flora at the rocky base, superficial beauty**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 23：山地剝 (Id: 23)
* **概念**：山（艮） + 地（坤）（高山受風雨侵蝕，剝落於平地）。代表「剝落、衰敗、面臨崩解」。
* **Prompt**：
    > **A towering, ancient mountain peak slowly crumbling and eroding into the vast, flat dark earth below, steep cliffs shedding rocks in silent slow motion, a sense of inevitable decay and stark reality**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 24：地雷復 (Id: 24)
* **概念**：地（坤） + 雷（震）（雷聲隱於地下，一陽初生）。代表「冬至、轉機、黑暗中迎來第一道曙光」。
* **Prompt**：
    > **A single, vibrant golden spark of lightning awakening deep beneath a frozen, silent expanse of dark earth, the very first pulse of spring returning to a dormant world, quiet hope and rebirth**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 25：天雷無妄 (Id: 25)
* **概念**：天（乾） + 雷（震）（天下雷行，自然運作無虛假）。代表「純真、順其自然、意料之外的震動」。
* **Prompt**：
    > **Pure, chaotic golden lightning branching wildly across a vast, empty, flawless white sky, sudden natural phenomena occurring without warning over a serene landscape, untamed cosmic energy**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 26：山天大畜 (Id: 26)
* **概念**：山（艮） + 天（乾）（山中藏著整片天空）。代表「巨大的能量被蓄積、蘊藏著無限潛力」。
* **Prompt**：
    > **A massive, solid black mountain containing a swirling, glowing cosmos and sky within its hollow core, immense celestial energy perfectly held and contained by unbreakable stone, ultimate potential**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 27：山雷頤 (Id: 27)
* **概念**：山（艮） + 雷（震）（上下皆實，中間空虛，形如張開的嘴巴）。代表「頤養、進食、修身養性」。
* **Prompt**：
    > **A deep, majestic valley uniquely shaped like an open mouth, framed by solid dark mountain peaks above and vibrant, electrifying energy rumbling below, a mystical source of life and nourishment**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 28：澤風大過 (Id: 28)
* **概念**：澤（兌） + 風/木（巽）（澤水淹沒了樹木，棟樑承受不住重壓）。代表「負荷過重、非常行動、壓力達到臨界點」。
* **Prompt**：
    > **A massive, ancient willow tree bending precariously under the overwhelming weight of a dark, rising flood, roots struggling to hold against the submerged earth, immense tension and the verge of collapse**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 29：坎為水 (Id: 29)
* **概念**：水（坎） + 水（坎）（重重險阻，深淵疊著深淵）。代表「危險、陷阱、但在深淵中保持水流不息」。
* **Prompt**：
    > **A terrifying, seemingly bottomless oceanic trench with turbulent, dark whirlpools crashing against sharp, hidden rocks, relentless and dangerous flow of deep water, profound abyss**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 30：離為火 (Id: 30)
* **概念**：火（離） + 火（離）（光明相繼，烈焰依附於可燃之物燃燒）。代表「光明、智慧、燃燒與依附」。
* **Prompt**：
    > **Twin radiant, ethereal suns blazing intensely and endlessly in a stark, empty sky, casting brilliant, piercing rays of light over a barren landscape, ultimate illumination and clinging energy**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 31：澤山咸 (Id: 31)
* **概念**：澤（兌） + 山（艮）（山頂有湖泊，澤水下滲滋潤山體）。代表「感應、吸引、少男少女純潔的互相傾慕」。
* **Prompt**：
    > **A breathtaking, perfectly tranquil crystal lake resting at the very summit of a majestic mountain, its gentle waters slowly seeping into the ancient stone, perfect mutual harmony and silent attraction**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 32：雷風恆 (Id: 32)
* **概念**：雷（震） + 風（巽）（雷與風長久相伴，自然運作的常態）。代表「恆久、穩定、堅持不懈的常道」。
* **Prompt**：
    > **An ancient, unyielding bamboo forest standing resolute and graceful amidst an endless storm of howling winds and distant, subtle golden lightning, the beauty of enduring strength and timeless consistency**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 33：天山遯 (Id: 33)
* **概念**：天（乾） + 山（艮）（天下有山，山雖高，天卻一直向後退卻）。代表「退避、隱居、遠離小人」。
* **Prompt**：
    > **A solitary, rugged mountain peak reaching upwards, while vast, luminous clouds and the majestic sky seem to endlessly pull away into the profound distance, a deep sense of withdrawal, isolation, and unreachability**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 34：雷天大壯 (Id: 34)
* **概念**：雷（震） + 天（乾）（雷聲響徹天際，陽氣極盛）。代表「極大的力量、氣勢強盛、不可阻擋」。
* **Prompt**：
    > **Massive, aggressive bolts of golden lightning violently crashing across the entire vault of an open, endless sky, an overwhelming display of cosmic power and masculine energy tearing through the clouds**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 35：火地晉 (Id: 35)
* **概念**：火（離） + 地（坤）（太陽從地平線升起，光耀大地）。代表「晉升、日出、光明正大地前進」。
* **Prompt**：
    > **A glorious, radiant sunrise emerging directly from a perfectly flat, dark horizon, spreading striking beams of golden light across the vast, awakening plains, dawn, rapid progress and rising prominence**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 36：地火明夷 (Id: 36)
* **概念**：地（坤） + 火（離）（太陽沉入地底，光明被掩蓋）。代表「日落、黑暗時期、隱藏光芒以求自保」。
* **Prompt**：
    > **A glowing, divine sun slowly sinking and being completely swallowed by heavy, dark, enclosing earth, entering a deep subterranean cavern, the painful extinguishing of light, hidden brilliance in times of extreme darkness**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 37：風火家人 (Id: 37)
* **概念**：風（巽） + 火（離）（火在內部燃燒，熱氣上升形成風）。代表「家庭、內部的和諧與溫暖」。
* **Prompt**：
    > **A warm, glowing hearth fire gently radiating inside a dark, serene bamboo dwelling, soft wisps of warm smoke rising gracefully into the night air, intimate harmony and internal warmth**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 38：火澤睽 (Id: 38)
* **概念**：火（離） + 澤（兌）（火向上燃燒，水向下流動）。代表「背道而馳、對立、分離」。
* **Prompt**：
    > **A stark, dramatic visual split between fierce golden flames rising fiercely into the sky and calm, heavy dark waters pooling downwards into a deep lake, two opposing forces moving apart in perfect symmetry**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 39：水山蹇 (Id: 39)
* **概念**：水（坎） + 山（艮）（高山之前有險惡的冰水阻擋）。代表「險阻、跋涉艱難、寸步難行」。
* **Prompt**：
    > **A treacherous, towering dark mountain peak completely blocked by freezing, turbulent rapids and heavy, dangerous rain, a steep and impassable path, immense hardship and struggle**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 40：雷水解 (Id: 40)
* **概念**：雷（震） + 水（坎）（春雷陣陣，帶來春雨解開冰封）。代表「解放、危機解除、冰雪消融」。
* **Prompt**：
    > **A sudden, brilliant flash of golden lightning shattering a heavy, dark storm cloud, releasing a gentle, refreshing rain over a thawing, ancient landscape, liberation and the sudden release of deep tension**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 41：山澤損 (Id: 41)
* **概念**：山（艮） + 澤（兌）（山下的湖水蒸發，化為雲氣滋潤高山）。代表「減損下位以增益上位、犧牲與奉獻」。
* **Prompt**：
    > **The still, dark waters of a deep lake slowly evaporating into luminous, ascending mist, humbly sacrificing its depth to nourish the towering, majestic mountain peak above**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 42：風雷益 (Id: 42)
* **概念**：風（巽） + 雷（震）（狂風與雷鳴互相激盪，聲勢浩大）。代表「增益、擴張、相輔相成」。
* **Prompt**：
    > **A massive, dynamic swirl of howling winds perfectly synchronized with echoing strikes of golden lightning across a vast, dark canyon, energies amplifying each other in wild, expansive harmony**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 43：澤天夬 (Id: 43)
* **概念**：澤（兌） + 天（乾）（湖水高漲至天上，隨時可能潰堤化為暴雨）。代表「決斷、突破、將能量一次釋放」。
* **Prompt**：
    > **A massive, overwhelming body of dark water suspended precariously high in the glowing, endless sky, on the exact verge of a spectacular, decisive breakthrough, overwhelming tension ready to burst**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 44：天風姤 (Id: 44)
* **概念**：天（乾） + 風（巽）（天下起風，風吹遍大地的每一個角落）。代表「相遇、偶然的邂逅、無孔不入的影響力」。
* **Prompt**：
    > **A single, profound gust of ethereal wind sweeping gracefully beneath the vast, towering dome of a majestic white sky, bending ancient bamboo forests in a sudden, fateful encounter**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 45：澤地萃 (Id: 45)
* **概念**：澤（兌） + 地（坤）（水往低處流，在大地上匯聚成湖泊）。代表「聚集、會合、眾志成城」。
* **Prompt**：
    > **Countless subtle streams of dark, tranquil water elegantly converging and pooling together to form a vast, serene lake upon an endless flat earth, harmonious gathering of natural forces**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 46：地風升 (Id: 46)
* **概念**：地（坤） + 風/木（巽）（樹木從地底生長而出，不斷向上拔高）。代表「上升、穩步前進、不斷成長」。
* **Prompt**：
    > **A single, massive ancient bamboo trunk glowing with vital golden energy, steadily and powerfully pushing upwards through heavy, dark soil towards the light, relentless and elegant growth from the depths**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 47：澤水困 (Id: 47)
* **概念**：澤（兌） + 水（坎）（湖泊裡的水漏到了底下，導致上方乾涸）。代表「困頓、枯竭、受限於絕境」。
* **Prompt**：
    > **A stark, severely cracked and bone-dry lakebed under a heavy, oppressive sky, while a dark, inaccessible river flows silently deep underground, extreme exhaustion and isolation, profound stillness**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 48：水風井 (Id: 48)
* **概念**：水（坎） + 風/木（巽）（木桶下到水裡取水）。代表「源源不絕的滋養、深層的智慧與資源」。
* **Prompt**：
    > **A perfectly round, ancient stone well hidden deep within a dark, silent bamboo forest, its profound depths glowing with pure, still, golden water, an endless source of life and inner wisdom**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 49：澤火革 (Id: 49)
* **概念**：澤（兌） + 火（離）（水火相剋，火旺則水乾，水大則火滅）。代表「劇變、革命、徹底的去舊佈新」。
* **Prompt**：
    > **A dramatic, violent clash between a blazing, ethereal golden fire and a heavy, dark lake, the intense heat instantly transforming the turbulent water into a massive pillar of rising steam, radical transformation and destruction of the old**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 50：火風鼎 (Id: 50)
* **概念**：火（離） + 風/木（巽）（以木生火，烹煮食物的巨鼎）。代表「穩重、建立新氣象、轉化與昇華」。
* **Prompt**：
    > **A majestic, monolithic ancient bronze cauldron standing resolutely over a roaring, elegant golden fire fueled by sweeping winds, alchemy, profound transformation and divine nourishment**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 51：震為雷 (Id: 51)
* **概念**：雷（震） + 雷（震）（雙重雷擊，驚天動地）。代表「巨大的震動、恐懼後的覺醒、打破沉悶」。
* **Prompt**：
    > **A terrifying, awe-inspiring display of chaotic, double golden lightning strikes violently shattering massive, ancient dark basalt rocks, pure explosive energy and profound awakening**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 52：艮為山 (Id: 52)
* **概念**：山（艮） + 山（艮）（群山重疊，靜止不動）。代表「絕對的靜止、冥想、停頓與沉穩」。
* **Prompt**：
    > **Endless, majestic layers of immovable dark mountain peaks rising perfectly still in a vast, silent sea of pure white mist, absolute stillness, profound meditation and eternal solidity**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 53：風山漸 (Id: 53)
* **概念**：風/木（巽） + 山（艮）（樹木在山上扎根生長，進展緩慢但堅定）。代表「循序漸進、穩健的成長」。
* **Prompt**：
    > **Ancient, elegant pine trees with glowing golden roots slowly but relentlessly growing on the steep, solid cliff of a silent dark mountain, enduring the gentle wind over deep time, gradual but unstoppable growth**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 54：雷澤歸妹 (Id: 54)
* **概念**：雷（震） + 澤（兌）（雷聲震動湖面，打破了平靜）。代表「衝動、反常規的結合、躁動不安」。
* **Prompt**：
    > **Sudden, chaotic golden lightning violently striking the surface of a previously calm, dark lake, causing turbulent splashes and restless ripples, intense energy disrupting profound peace**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 55：雷火豐 (Id: 55)
* **概念**：雷（震） + 火（離）（雷電交加，光焰萬丈）。代表「豐盛、極致的巔峰、能量大爆發」。
* **Prompt**：
    > **A spectacular, overwhelming display of blazing golden fire fiercely illuminating dark, heavy clouds, perfectly synchronized with explosive golden lightning, the absolute climax of cosmic energy and breathtaking abundance**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 56：火山旅 (Id: 56)
* **概念**：火（離） + 山（艮）（火在山上蔓延，不會在一個地方停留太久）。代表「旅行、漂泊、轉瞬即逝的過客」。
* **Prompt**：
    > **A solitary, restless golden flame rapidly burning and traveling across the high, stark ridges of a dark, silent mountain peak, a fleeting and wandering light in the vast, empty wilderness**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 57：巽為風 (Id: 57)
* **概念**：風（巽） + 風（巽）（微風相繼吹拂，無孔不入）。代表「順從、滲透、潛移默化的深遠影響」。
* **Prompt**：
    > **Countless ethereal, flowing lines of wind gently and persistently sweeping through an endless, ancient bamboo forest, bending the dark stalks in perfect, graceful unison, deep and silent penetration**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 58：兌為澤 (Id: 58)
* **概念**：澤（兌） + 澤（兌）（兩座湖泊相連，水流互相滋潤）。代表「喜悅、交流、和諧的共鳴」。
* **Prompt**：
    > **Two perfectly serene, connected dark lakes reflecting pure, soft moonlight, their waters gently overflowing and mingling with each other in profound harmony, quiet joy and endless mutual nourishment**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 59：風水渙 (Id: 59)
* **概念**：風（巽） + 水（坎）（風吹過水面，將水波吹散化為雲氣）。代表「渙散、消解冰冷與僵局、散佈」。
* **Prompt**：
    > **A strong, ethereal wind gracefully sweeping across the surface of a dark, deep ocean, breaking the surface tension and scattering turbulent waves into fine, glowing golden mist, the beautiful dispersion of heavy blockages**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 60：水澤節 (Id: 60)
* **概念**：水（坎） + 澤（兌）（湖泊的容量有限，堤壩節制了水的流動）。代表「節制、適度、竹子的節」。
* **Prompt**：
    > **A perfectly balanced, serene dark lake with distinct, elegant rock formations acting as natural dams, precisely controlling the flow of pure water, the profound beauty of limits and graceful moderation**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 61：風澤中孚 (Id: 61)
* **概念**：風（巽） + 澤（兌）（風吹動水面，內心如湖水般清澈，如中空的蘆葦）。代表「誠信、內心的真實、與神靈的感應」。
* **Prompt**：
    > **A perfectly hollow, delicate glowing golden reed floating peacefully in the exact center of a vast, tranquil dark lake, untouched by the gentle wind, profound inner sincerity and divine emptiness**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 62：雷山小過 (Id: 62)
* **概念**：雷（震） + 山（艮）（高山上有雷鳴，飛鳥掠過山巔）。代表「稍微過度、小事可做大事不宜、過渡時期」。
* **Prompt**：
    > **A single, delicate silhouette of a flying bird passing briefly beneath a low, rumbling thundercloud over a solid, silent dark mountain peak, fleeting moments and small transitions**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 63：水火既濟 (Id: 63)
* **概念**：水（坎） + 火（離）（水在火上，完美烹調，達到平衡）。代表「完成、完美狀態、但也意味著即將走向反面」。
* **Prompt**：
    > **A perfect, harmonious equilibrium where gentle, glowing golden flames sit flawlessly beneath a calm, boiling cauldron of dark water, delicate absolute balance and perfect completion, fragile perfection**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4

#### 卦 64：火水未濟 (Id: 64)
* **概念**：火（離） + 水（坎）（火往上燒，水往下流，互不交集）。代表「尚未完成、充滿無限的可能性與新的開始」。
* **Prompt**：
    > **A striking, epic contrast of blazing golden flames endlessly reaching upward into the sky while deep, dark water flows eternally downward into an abyss, moving in opposite directions, the raw, unfinished potential of the cosmos, endless cycles**, surreal oriental ink painting style, Zen atmosphere, minimalism, ethereal lighting, mysterious mist, soft edge, sharp focus on central element, monochromatic black and white with subtle metallic gold accents, cgsociety, 8k, highly detailed. --ar 3:4



## 執行與儲存路徑
-   **檔案命名**：`assets/images/hexagrams/{id}.png` (例如：`assets/images/hexagrams/1.png`)
-   **解析度**：至少 1024x1365 (對應 3:4 比例)，建議與塔羅牌專案保持一致。
-   **UI 整合**：在 Streamlit 的 `app.py` 中，讀取 JSON 資料後，根據卦象 ID 同時顯示生成的意境圖，並在圖片上方「疊加」或在旁邊「並列」由程式碼畫出的黑白爻象圖。


