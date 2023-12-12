import logging
import os
import requests
from forex_python.converter import CurrencyCodes ##
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from telegram.ext import CommandHandler, CallbackContext
from telegram import Update
import emoji
import random

TOKEN = '<INSERT TOKEN HERE>'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
currencies = [
'AED - United Arab Emirates Dirham', 
'AFN - Afghan Afghani', 
'ALL - Albanian Lek', 
'AMD - Armenian Dram', 
'ANG - Netherlands Antillean Guilder', 
'AOA - Angolan Kwanza', 
'ARS - Argentine Peso', 
'AUD - Australian Dollar', 
'AWG - Aruban Florin', 
'AZN - Azerbaijani Manat', 
'BAM - Bosnia-Herzegovina Convertible Mark', 
'BBD - Barbadian Dollar', 
'BDT - Bangladeshi Taka', 
'BGN - Bulgarian Lev', 
'BHD - Bahraini Dinar', 
'BIF - Burundian Franc', 
'BMD - Bermudan Dollar', 
'BND - Brunei Dollar', 
'BOB - Bolivian Boliviano', 
'BRL - Brazilian Real', 
'BSD - Bahamian Dollar', 
'BTC - Bitcoin', 
'BTN - Bhutanese Ngultrum', 
'BWP - Botswanan Pula', 
'BYN - Belarusian Ruble', 
'BZD - Belize Dollar', 
'CAD - Canadian Dollar', 
'CDF - Congolese Franc', 
'CHF - Swiss Franc', 
'CLF - Chilean Unit of Account (UF)', 
'CLP - Chilean Peso', 
'CNH - Chinese Yuan (Offshore)', 
'CNY - Chinese Yuan', 
'COP - Colombian Peso', 
'CRC - Costa Rican Colón', 
'CUC - Cuban Convertible Peso', 
'CUP - Cuban Peso', 
'CVE - Cape Verdean Escudo', 
'CZK - Czech Republic Koruna', 
'DJF - Djiboutian Franc', 
'DKK - Danish Krone', 
'DOP - Dominican Peso', 
'DZD - Algerian Dinar', 
'EGP - Egyptian Pound', 
'ERN - Eritrean Nakfa', 
'ETB - Ethiopian Birr', 
'EUR - Euro', 
'FJD - Fijian Dollar', 
'FKP - Falkland Islands Pound', 
'GBP - British Pound Sterling', 
'GEL - Georgian Lari', 
'GGP - Guernsey Pound', 
'GHS - Ghanaian Cedi', 
'GIP - Gibraltar Pound', 
'GMD - Gambian Dalasi', 
'GNF - Guinean Franc', 
'GTQ - Guatemalan Quetzal', 
'GYD - Guyanaese Dollar', 
'HKD - Hong Kong Dollar', 
'HNL - Honduran Lempira', 
'HRK - Croatian Kuna', 
'HTG - Haitian Gourde', 
'HUF - Hungarian Forint', 
'IDR - Indonesian Rupiah', 
'ILS - Israeli New Sheqel', 
'IMP - Manx pound', 
'INR - Indian Rupee', 
'IQD - Iraqi Dinar', 
'IRR - Iranian Rial', 
'ISK - Icelandic Króna', 
'JEP - Jersey Pound', 
'JMD - Jamaican Dollar', 
'JOD - Jordanian Dinar', 
'JPY - Japanese Yen', 
'KES - Kenyan Shilling', 
'KGS - Kyrgystani Som', 
'KHR - Cambodian Riel', 
'KMF - Comorian Franc', 
'KPW - North Korean Won', 
'KRW - South Korean Won', 
'KWD - Kuwaiti Dinar', 
'KYD - Cayman Islands Dollar', 
'KZT - Kazakhstani Tenge', 
'LAK - Laotian Kip', 
'LBP - Lebanese Pound', 
'LKR - Sri Lankan Rupee', 
'LRD - Liberian Dollar', 
'LSL - Lesotho Loti', 
'LYD - Libyan Dinar', 
'MAD - Moroccan Dirham', 
'MDL - Moldovan Leu', 
'MGA - Malagasy Ariary', 
'MKD - Macedonian Denar', 
'MMK - Myanma Kyat', 
'MNT - Mongolian Tugrik', 
'MOP - Macanese Pataca', 
'MRO - Mauritanian Ouguiya (pre-2018)', 
'MRU - Mauritanian Ouguiya', 
'MUR - Mauritian Rupee', 
'MVR - Maldivian Rufiyaa', 
'MWK - Malawian Kwacha', 
'MXN - Mexican Peso', 
'MYR - Malaysian Ringgit', 
'MZN - Mozambican Metical', 
'NAD - Namibian Dollar', 
'NGN - Nigerian Naira', 
'NIO - Nicaraguan Córdoba', 
'NOK - Norwegian Krone', 
'NPR - Nepalese Rupee', 
'NZD - New Zealand Dollar', 
'OMR - Omani Rial', 
'PAB - Panamanian Balboa', 
'PEN - Peruvian Nuevo Sol', 
'PGK - Papua New Guinean Kina', 
'PHP - Philippine Peso', 
'PKR - Pakistani Rupee', 
'PLN - Polish Zloty', 
'PYG - Paraguayan Guarani', 
'QAR - Qatari Rial', 
'RON - Romanian Leu', 
'RSD - Serbian Dinar', 
'RUB - Russian Ruble', 
'RWF - Rwandan Franc', 
'SAR - Saudi Riyal', 
'SBD - Solomon Islands Dollar', 
'SCR - Seychellois Rupee', 
'SDG - Sudanese Pound', 
'SEK - Swedish Krona', 
'SGD - Singapore Dollar', 
'SHP - Saint Helena Pound', 
'SLL - Sierra Leonean Leone', 
'SOS - Somali Shilling', 
'SRD - Surinamese Dollar', 
'SSP - South Sudanese Pound', 
'STD - São Tomé and Príncipe Dobra (pre-2018)', 
'STN - São Tomé and Príncipe Dobra', 
'SVC - Salvadoran Colón', 
'SYP - Syrian Pound', 
'SZL - Swazi Lilangeni', 
'THB - Thai Baht', 
'TJS - Tajikistani Somoni', 
'TMT - Turkmenistani Manat', 
'TND - Tunisian Dinar', 
'TRY - Turkish Lira', 
'TTD - Trinidad and Tobago Dollar', 
'TWD - New Taiwan Dollar', 
'TZS - Tanzanian Shilling', 
'UAH - Ukrainian Hryvnia', 
'UGX - Ugandan Shilling', 
'USD - United States Dollar', 
'UYU - Uruguayan Peso', 
'UZS - Uzbekistan Som', 
'VEF - Venezuelan Bolívar Fuerte (Old)', 
'VES - Venezuelan Bolívar Soberano', 
'VND - Vietnamese Dong', 
'VUV - Vanuatu Vatu', 
'WST - Samoan Tala', 
'XAF - CFA Franc BEAC', 
'XAG - Silver Ounce', 
'XAU - Gold Ounce', 
'XCD - East Caribbean Dollar', 
'XDR - Special Drawing Rights', 
'XOF - CFA Franc BCEAO', 
'XPD - Palladium Ounce', 
'XPF - CFP Franc', 
'XPT - Platinum Ounce', 
'YER - Yemeni Rial', 
'ZAR - South African Rand', 
'ZMW - Zambian Kwacha'
]
happy_emojis = ["\U0001F60A", "\U0001F603", "\U0001F601", "\U0001F604", "\U0001F606", "\U0001F61C", "\U0001F61D", "\U0001F61B", "\U0001F617", "\U0001F619", "\U0001F973", "\U0001F929", "\U0001F970", "\U0001F917", "\U0001F92D", "\U0001F60A", "\U0001F92A", "\U0001F92D", "\U0001F973"]
sus_emojis = ["\U0001F928", "\U0001F9D0", "\U0001F914", "\U0001F92B", "\U0001F925", "\U0001F922", "\U0001F92E", "\U0001F92F", "\U0001F914"]
users = {}

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    users[user_id] = {'from_currency': None, 'to_currency': None}
    random_emoji = random.choice(happy_emojis)
    await bot.send_message(chat_id, f'Hi! My name is CCB, your personal Currency Converter Bot {random_emoji} \n \nTo view a full list of currencies available, type /list \nTo view help page, type /help\n \nPlease choose the currencies you would like to convert. \n \nFor example: "GBP EUR"')

@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await bot.send_message(chat_id, f'Commands: \nTo restart bot, type /start\nTo view a full list of currencies available, type /list \nTo change currencies, type /change\nTo view help page, type /help')

@dp.message_handler(commands=['list'])
async def list_currencies(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    users[user_id]['from_currency'] = None
    users[user_id]['to_currency'] = None
    await bot.send_message(chat_id, '\n'.join(currencies))
    await bot.send_message(chat_id, f'Please choose the currencies you would like to convert. \n \nFor example: "GBP EUR"')

@dp.message_handler(commands=['about'])
async def list_currencies(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await bot.send_message(chat_id, f'Rates are updated around midnight UTC every working day. Sources used:\n\nEuropean Central Bank\nhttp://www.ecb.europa.eu/')

@dp.message_handler()
async def convert_currency(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if users[user_id]['from_currency'] is None or users[user_id]['to_currency'] is None:
        try:
            from_currency, to_currency = message.text.split()
            users[user_id]['from_currency'] = from_currency.upper()
            users[user_id]['to_currency'] = to_currency.upper()
            random_emoji = random.choice(happy_emojis)
            url = 'https://api.exchangerate.host/convert?from=' + from_currency + '&to=' + to_currency + '&source=ecb'
            response = requests.get(url)
            data = response.json()
            rate = data['info']['rate']
            rate_formatted = '{:,.4f}'.format(rate)
            await bot.send_message(chat_id, f"You are converting {from_currency.upper()} to {to_currency.upper()} {random_emoji} \n \n(Current rate: {rate_formatted}) \n \nPlease enter the value you want to convert:")
        except (ValueError, KeyError):
            random_emoji = random.choice(sus_emojis)
            await bot.send_message(chat_id, f'{random_emoji} Sorry, I could not process your request \n \nPlease choose the currencies you would like to convert. \n \nFor example: "GBP EUR"')
    elif message.text.lower() in ['change', '/change']:
        users[user_id]['from_currency'] = None
        users[user_id]['to_currency'] = None
        random_emoji = random.choice(happy_emojis)
        await bot.send_message(chat_id, f'Please choose the currencies you would like to convert. \n \nFor example: "GBP EUR"')
    else:
        try:
            value = float(message.text)
            from_currency = users[user_id]['from_currency']
            to_currency = users[user_id]['to_currency']
            url = 'https://api.exchangerate.host/convert?from=' + from_currency + '&to=' + to_currency + '&source=ecb'
            response = requests.get(url)
            data = response.json()
            rate = data['info']['rate']
            result = rate * value
            currency_codes = CurrencyCodes()
            from_currency_symbol = currency_codes.get_symbol(from_currency)
            if not from_currency_symbol:
                from_currency_symbol = from_currency
            to_currency_symbol = currency_codes.get_symbol(to_currency)
            if not to_currency_symbol:
                to_currency_symbol = to_currency
            result_formatted = to_currency_symbol + '{:,.2f}'.format(result)
            rate_formatted = to_currency_symbol + '{:,.2f}'.format(rate)
            await bot.send_message(chat_id, f'{from_currency_symbol}{value:,.2f} is equal to {result_formatted} \n \n({from_currency_symbol}1.00 = {rate_formatted})\n \nPlease enter the value you want to convert:')
        except:
            try:
                from_currency, to_currency = message.text.split()
                users[user_id]['from_currency'] = from_currency.upper()
                users[user_id]['to_currency'] = to_currency.upper()
                random_emoji = random.choice(happy_emojis)
                url = 'https://api.exchangerate.host/convert?from=' + from_currency + '&to=' + to_currency + '&source=ecb'
                response = requests.get(url)
                data = response.json()
                rate = data['info']['rate']
                rate_formatted = '{:,.4f}'.format(rate)
                await bot.send_message(chat_id, f"You are converting {from_currency.upper()} to {to_currency.upper()} {random_emoji} \n \n(Current rate: {rate_formatted}) \n \nPlease enter the value you want to convert:")
            except:
                random_emoji = random.choice(sus_emojis)
                await bot.send_message(chat_id, f"{random_emoji} Sorry, I could not process your request \n \nPlease enter a valid number.")
    
from telegram.ext import CommandHandler

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)