from bing_image_downloader import downloader

places = [
    "Taj Mahal",
    "Qutub Minar",
    "Red Fort",
    "Gateway of India",
    "India Gate",
    "Hawa Mahal",
    "Amber Fort",
    "City Palace Jaipur",
    "Lotus Temple",
    "Akshardham Temple Delhi",
    "Charminar",
    "Golconda Fort",
    "Mysore Palace",
    "Gol Gumbaz",
    "Hampi Temple",
    "Virupaksha Temple",
    "Belur Halebidu Temple",
    "Somnath Temple Karnataka",
    "Badami Caves",
    "Pattadakal Temples",
    "Chitradurga Fort",
    "Shravanabelagola",
    "Bangalore Palace",
    "Gaganchukki Falls",
    "Elephanta Caves",
    "Ajanta Caves",
    "Ellora Caves",
    "Victoria Memorial",
    "Howrah Bridge",
    "Sanchi Stupa",
    "Khajuraho Temples",
    "Rani Ki Vav",
    "Sun Temple Konark",
    "Meenakshi Amman Temple",
    "Brihadeeswarar Temple",
    "Rameshwaram Temple",
    "Mahabodhi Temple",
    "Golden Temple Amritsar",
    "Humayun's Tomb",
    "Fatehpur Sikri",
    "Jantar Mantar Jaipur",
    "Rashtrapati Bhavan",
    "Vivekananda Rock Memorial",
    "Cellular Jail Andaman",
    "Kashi Vishwanath Temple",
    "Badrinath Temple",
    "Somnath Temple Gujarat",
    "Kedarnath Temple",
    "Sultan Battery Mangalore"
]

for place in places:
    print(f"\n📥 Downloading images for: {place}")
    downloader.download(
        place,                # <-- OLD syntax
        limit=15,
        output_dir='dataset',
        adult_filter_off=True,
        force_replace=False
    )