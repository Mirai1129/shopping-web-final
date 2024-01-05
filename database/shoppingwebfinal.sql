-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-01-05 14:18:07
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `shoppingwebfinal`
--

-- --------------------------------------------------------

--
-- 資料表結構 `member`
--

CREATE TABLE `member` (
  `memberId` int(11) NOT NULL,
  `firstName` varchar(10) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `displayName` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `address` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `ordersheet`
--

CREATE TABLE `ordersheet` (
  `orderId` int(11) NOT NULL,
  `firstName` int(20) NOT NULL,
  `lastName` int(45) NOT NULL,
  `address` int(45) NOT NULL,
  `phone` int(45) NOT NULL,
  `email` int(45) NOT NULL,
  `memberId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `ordersheet_has_product`
--

CREATE TABLE `ordersheet_has_product` (
  `orderId` int(11) NOT NULL,
  `productId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `product`
--

CREATE TABLE `product` (
  `productId` int(11) NOT NULL,
  `productName` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `summary` varchar(200) NOT NULL,
  `category` varchar(20) NOT NULL,
  `information` varchar(400) NOT NULL,
  `introduction` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- 傾印資料表的資料 `product`
--

INSERT INTO `product` (`productId`, `productName`, `quantity`, `price`, `summary`, `category`, `information`, `introduction`) VALUES
(1, '毛茸茸大溫毯', 265, 857, '◆毛茸茸的材質\r\n◆大尺寸\r\n◆保暖性能\r\n◆多種顏色和設計\r\n◆易清潔', '毯子', '這樣的溫暖毯常常受到在冷天中渴望額外保暖的人們的歡迎，也可以用來裝飾家居，為房間增添溫馨感。', '毛茸茸的材質： 使用柔軟的、毛茸茸的材質，為長毛絨所製成。\n大尺寸： 設計為比標準毯子更大，可以完全覆蓋身體，讓人感到更包裹和溫暖。\n保暖性能： 具有優秀的保暖性能，使其成為冷天或冬季的理想選擇。\n多種顏色和設計： 提供多種顏色和設計選擇，以滿足不同人的風格和喜好。\n易清潔： 一些毯子可能採用易清潔的材質，方便日常保養。'),
(2, '天然乳膠枕', 635, 2888, '◆高含量97%天然乳膠枕\r\n◆深層睡眠的最後一塊拼圖\r\n◆Q彈支撐頭肩頸，側睡仰睡都有好眠\r\n◆饅頭枕適合每個人，穩固包覆頭頸\r\n◆狼牙枕適合仰睡者，服貼支撐頸椎\r\n◆SGS、ECO及LGA多重認證，無毒無甲醛', '枕頭', '乳膠枕的特色\r\n採用100%橡樹汁液製成的天然乳膠枕，含有橡樹蛋白酶能抑制細菌和螨蟲孳生，富含彈性不易扁塌與變形，且支撐力強，對頸部提供優異的支撐力，能協助改善使用者的睡姿，緩解肩頸酸痛等問題；其耐用程度高過其他類型的枕頭，如記憶枕、羽絨枕，正常使用和定期保養能夠讓乳膠枕的壽命長達8 - 10年；此外乳膠的蜂窩狀結構，有助於透氣散熱，保持舒適的溫度來提升睡眠品質，以下整理乳膠枕的特色，提供給您參考：\r\n◆防蟎抗菌\r\n◆安全無毒\r\n◆Q彈支撐\r\n◆緩解痠痛\r\n◆調整睡姿\r\n◆透氣散熱\r\n◆經久耐用\r\n◆不易扁塌', '無論你仰睡側睡，只給您肩頸放鬆舒適好眠，讓您不再剛起床肩頸就緊繃痠痛，好像沒睡好頭好暈好昏，一早鼻子癢噴嚏打不停。健康純淨 睡眠環境高純度97%天然乳膠枕，其含有的橡樹蛋白酶，能抑制蟎蟲滋生及防止蚊蟲靠近，也比較不會引起過敏症狀，對人體安全無毒又環境友善。柔軟Ｑ彈全面支撐，能夠適應睡眠者的各種睡姿，自然貼合頸部曲線的高彈性支撐，躺下時能平均受力並緩衝頭部壓力，有效舒緩頭部及肩頸的緊繃不適。透氣舒適 整夜好眠乳膠蜂窩狀氣孔結構具有良好的透氣性，快速散發人體產生的熱能，並幫助排除濕氣，來提升您的睡眠品質，讓您擁有整夜好眠到天亮。'),
(3, '天絲床包組 (床包+枕套)', 352, 4286, '◆親膚柔滑 | 抑菌抗敏 | 吸濕排汗 | 耐用耐洗\r\n◆100%萊賽爾纖維60支緊密編織\r\n◆REFIBRATM 科技永續自然0浪費\r\n◆天然纖維抑菌抗敏，守護您的肌膚\r\n◆涼爽舒適親膚，安穩睡眠一整晚', '枕頭', '天絲的成分由尤加利樹中提煉而成，製作過程中不會產生過多污染和廢料，是一款對地球環境友善的綠色纖維。天絲（萊賽爾Lyocell）纖維製作而成的紡織品會比棉更吸水、比絲綢更柔軟、比麻料更涼爽親膚、比人造纖維更堅韌有彈性。', '天絲的成分由尤加利樹中提煉而成，製作過程中不會產生過多污染和廢料，是一款對地球環境友善的綠色纖維。天絲（萊賽爾Lyocell）纖維製作而成的紡織品會比棉更吸水、比絲綢更柔軟、比麻料更涼爽親膚、比人造纖維更堅韌有彈性。'),
(4, '【TRUESTUFF丹麥有機棉】赫辛基 平單被單組 丹麥原裝進口', 58, 25269, '◆330支紗有機棉寢具柔軟細緻，丹麥原裝進口。\r\n◆有機棉材質，自然法則下栽植棉花。\r\n◆絕不使用殺蟲劑、除草劑、枯葉劑等化學添加物。\r\n◆環保愛地球。不使用化學添加劑=減少過敏來源。', '棉被', '本產品免費提供平單改床包服務，若有此需求請在訂購單的備註欄位標註＂平單改床包＂，收到你的訂購單後，我們將盡快與您聯繫說明。', '來自丹麥有機棉品牌，最真實且簡約的時尚。符合GOTS標準，天然有機棉原裝進口品牌。採用歐洲當地種植的有機棉花。最天然的時尚簡約，並採用低彩度、柔和的設計，輕鬆打造北歐極簡居家生活。有機棉完全不含螢光劑、甲醛、農藥等任何有害物質，不導致過敏，使用更安心。舒適透氣，無添加任何化學物質，例如柔軟劑。越洗越柔軟、舒適透氣。環保健康，從種植到生產，不會對大地造成負擔，更不會危害到農民的健康。GOTS有機棉花認證，最友善肌膚材質。\r\nGOTS（Global Organic Textile Standard）是一個國際性的有機紡織品標準，它確保紡織品在生產過程中符合環保和社會責任的標準。對於有機棉花來說，GOTS認證確保了相應產品的有機栽培和加工標準。\r\n以下是GOTS有機棉花認證的一些主要要點：\r\n有機栽培： GOTS要求有機棉花必須是在不使用合成化肥、除草劑和有毒農藥的情況下種植的。農民必須遵從有機農業標準，以確保土壤和生態系統的健康。\r\n環境友好加工： 在棉花的加工過程中，GOTS要求使用環保的加工技術，並禁止使用許多有害的化學物質。這包括染料和化學品的使用，以確保產品的生產不對環境造成傷害。\r\n社會責任： GOTS關注社會方面的責任，確保生產者在生產過程中獲得公平待遇，包括合理的工資和工作條件。這有助於確保生產環節中的工人受到尊重和公平對待。\r\n整體產品標準： GOTS不僅僅關注原材料的有機性，還關注整個產品的環保性。這包括製造、包裝、標籤和負責任的社會實踐等方面。\r\n如果一個有機棉花產品擁有GOTS認證，這意味著它符合該標準的所有相關標準，從而提供了一個可靠的標誌，讓消費者能夠識別和選擇環保和社會負責的產品。');

-- --------------------------------------------------------

--
-- 資料表結構 `shoppingcart`
--

CREATE TABLE `shoppingcart` (
  `shoppingCartId` int(11) NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `memberId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`memberId`);

--
-- 資料表索引 `ordersheet`
--
ALTER TABLE `ordersheet`
  ADD PRIMARY KEY (`orderId`),
  ADD KEY `memberId` (`memberId`);

--
-- 資料表索引 `ordersheet_has_product`
--
ALTER TABLE `ordersheet_has_product`
  ADD KEY `orderId` (`orderId`),
  ADD KEY `productId` (`productId`);

--
-- 資料表索引 `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`productId`);

--
-- 資料表索引 `shoppingcart`
--
ALTER TABLE `shoppingcart`
  ADD PRIMARY KEY (`shoppingCartId`),
  ADD KEY `memberId1` (`memberId`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `member`
--
ALTER TABLE `member`
  MODIFY `memberId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `ordersheet`
--
ALTER TABLE `ordersheet`
  MODIFY `orderId` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `product`
--
ALTER TABLE `product`
  MODIFY `productId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `shoppingcart`
--
ALTER TABLE `shoppingcart`
  MODIFY `shoppingCartId` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `ordersheet`
--
ALTER TABLE `ordersheet`
  ADD CONSTRAINT `memberId` FOREIGN KEY (`memberId`) REFERENCES `member` (`memberId`);

--
-- 資料表的限制式 `ordersheet_has_product`
--
ALTER TABLE `ordersheet_has_product`
  ADD CONSTRAINT `orderId` FOREIGN KEY (`orderId`) REFERENCES `ordersheet` (`orderId`),
  ADD CONSTRAINT `productId` FOREIGN KEY (`productId`) REFERENCES `product` (`productId`);

--
-- 資料表的限制式 `shoppingcart`
--
ALTER TABLE `shoppingcart`
  ADD CONSTRAINT `memberId1` FOREIGN KEY (`memberId`) REFERENCES `member` (`memberId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
