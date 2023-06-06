--
-- База данных: `lab4`
--

-- --------------------------------------------------------

--
-- Структура таблицы `backup`
--

CREATE TABLE `backup` (
  `Sizeofbackup` int(11) NOT NULL,
  `dateofbackup` date DEFAULT NULL,
  `infoaboutbackup` varchar(100) DEFAULT NULL,
  `User_username` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `backup`
--

INSERT INTO `backup` (`Sizeofbackup`, `dateofbackup`, `infoaboutbackup`, `User_username`) VALUES
(2022, '2023-05-05', 'Infffo', 'Andrew'),
(11211, '2022-06-06', 'Info', 'Andrew'),
(11222, '2022-06-07', 'Info', 'Andrew');

-- --------------------------------------------------------

--
-- Структура таблицы `dispatch`
--

CREATE TABLE `dispatch` (
  `Region_name` varchar(60) NOT NULL,
  `country_near_or_far_abroad` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `dispatch`
--

INSERT INTO `dispatch` (`Region_name`, `country_near_or_far_abroad`) VALUES
('Russia', 'Arkhangelsk');

-- --------------------------------------------------------

--
-- Структура таблицы `invoice`
--

CREATE TABLE `invoice` (
  `invoice_current_date` date NOT NULL,
  `company_name` varchar(60) DEFAULT NULL,
  `receiver_name` varchar(45) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `serial_of_document` int(11) DEFAULT NULL,
  `bank_number` int(11) DEFAULT NULL,
  `bank_name` varchar(45) DEFAULT NULL,
  `selling_price` int(11) DEFAULT NULL,
  `quantity_of_product` int(11) DEFAULT NULL,
  `individual` varchar(45) DEFAULT NULL,
  `legal_entity` varchar(45) DEFAULT NULL,
  `Address_Region_name` varchar(60) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `invoice`
--

INSERT INTO `invoice` (`invoice_current_date`, `company_name`, `receiver_name`, `number`, `serial_of_document`, `bank_number`, `bank_name`, `selling_price`, `quantity_of_product`, `individual`, `legal_entity`, `Address_Region_name`) VALUES
('2022-06-06', 'Comp', 'Rec', 2141, 212121, 234214, 'Ban', 21412, 2141211, 'Ind', 'Le', 'Russia'),
('2023-06-05', 'Co', 'Re', 21, 12, 31, 'Bannnnk', 245, 542, 'Iin', 'Leg', 'Russia');

-- --------------------------------------------------------

--
-- Структура таблицы `product`
--

CREATE TABLE `product` (
  `code_of_product` int(11) NOT NULL,
  `name_of_product` varchar(45) DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `username` varchar(25) NOT NULL,
  `surname` varchar(45) DEFAULT NULL,
  `userlogin` varchar(45) DEFAULT NULL,
  `userpassword` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `user`
--

INSERT INTO `user` (`user_id`, `username`, `surname`, `userlogin`, `userpassword`) VALUES
(4, 'AANNNDREEEW', 'Logushev', 'LOGANd', 'password'),
(1, 'Andrew', 'Logushev', 'Andrew.Logushev', 'password'),
(2, 'Andrewka', 'Logushevka', 'Logpass', 'password'),
(3, 'Andrewww', 'Logg', 'LoggAndrw', 'password');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `backup`
--
ALTER TABLE `backup`
  ADD PRIMARY KEY (`Sizeofbackup`);

--
-- Индексы таблицы `dispatch`
--
ALTER TABLE `dispatch`
  ADD PRIMARY KEY (`Region_name`);

--
-- Индексы таблицы `invoice`
--
ALTER TABLE `invoice`
  ADD PRIMARY KEY (`invoice_current_date`),
  ADD KEY `fk_Invoice_Dispatch_idx` (`Address_Region_name`);

--
-- Индексы таблицы `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`code_of_product`);

--
-- Индексы таблицы `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `backup`
--
ALTER TABLE `backup`
  ADD CONSTRAINT `fk_Backup_User1` FOREIGN KEY (`User_username`) REFERENCES `user` (`username`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ограничения внешнего ключа таблицы `invoice`
--
ALTER TABLE `invoice`
  ADD CONSTRAINT `fk_Invoice_Dispatch` FOREIGN KEY (`Address_Region_name`) REFERENCES `dispatch` (`Region_name`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

