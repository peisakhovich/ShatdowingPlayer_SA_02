select V.* from tts_voices as V INNER JOIN languages as L ON V.language_code = L.language_code
where L.language_code = 'pl' Or L.language_code = 'ru'