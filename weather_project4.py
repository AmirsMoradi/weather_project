import requests
import numpy as np
import matplotlib.pyplot as plt

API_KEY = "************************"

provinces_names = np.array(["Tehran", "Isfahan", "Mashhad", "Shiraz", "Tabriz", "Rasht", "Ahvaz",
                            "Kermanshah", "Kerman", "Yazd", "Qom", "Zahedan", "Sanandaj", "Bandar Abbas", "Zanjan"])

provinces_coords = np.array([
    [35.6892, 51.3890],  # Tehran
    [32.6539, 51.6660],  # Isfahan
    [36.2970, 59.6060],  # Mashhad
    [29.5918, 52.5837],  # Shiraz
    [38.0667, 46.2993],  # Tabriz
    [37.2808, 49.5831],  # Rasht
    [31.3183, 48.6692],  # Ahvaz
    [34.3142, 47.0650],  # Kermanshah
    [30.2839, 57.0834],  # Kerman
    [31.8974, 54.3678],  # Yazd
    [34.6401, 50.8764],  # Qom
    [29.4978, 60.8629],  # Zahedan
    [35.3091, 47.0029],  # Sanandaj
    [27.1832, 56.2666],  # Bandar Abbas
    [36.6736, 48.4787]  # Zanjan
])

#  Pollutants
labels = np.array(["pm2_5", "pm10", "co", "o3", "no2", "so2"])


def get_air_quality(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        air_quality = data["list"][0]["components"]
        return np.array([air_quality[label] for label in labels])
    else:
        print(f"Error fetching data for {lat}, {lon}: {response.status_code}")
        return np.zeros(len(labels))


data_matrix = np.zeros((provinces_coords.shape[0], labels.shape[0]))

for i in range(provinces_coords.shape[0]):
    data_matrix[i] = get_air_quality(provinces_coords[i][0], provinces_coords[i][1], API_KEY)

print("\nAir quality information for each province:\n")
for i, province in enumerate(provinces_names):
    print(f"province: {province}")
    for j, label in enumerate(labels):
        print(f"{label.upper()}: {data_matrix[i, j]:.2f} µg/m3")
    print("-" * 40)

mean_values = np.mean(data_matrix, axis=0)
std_values = np.std(data_matrix, axis=0)

fig, axs = plt.subplots(3, 2, figsize=(15, 12))
fig.suptitle("Comparison of Air Quality Across Provinces", fontsize=16)

axs = axs.flatten()

for i, label in enumerate(labels):
    values = data_matrix[:, i]

    axs[i].bar(provinces_names, values, color="skyblue")
    axs[i].set_title(f"{label.upper()} Levels")
    axs[i].set_xlabel('Provinces')
    axs[i].set_ylabel(f"{label.upper()} Concentration (µg/m3)")
    axs[i].tick_params(axis='x', rotation=45)

    axs[i].axhline(y=mean_values[i], color="r", linestyle="--", label=f"Mean {label.upper()}")
    axs[i].fill_between(range(len(provinces_names)), mean_values[i] - std_values[i], mean_values[i] + std_values[i],
                        color="orange", alpha=0.2, label=f"STD Range for {label.upper()}")

    axs[i].legend()

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig("air_quality_comparison.png", dpi=300)

plt.show()

print("\nAverage values of pollutants for all provinces:")
for i, label in enumerate(labels):
    print(f"{label.upper()} Mean: {mean_values[i]:.2f} µg/m3, STD: {std_values[i]:.2f} µg/m3")
