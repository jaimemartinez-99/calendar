<template>
  <div id="app" class="p-6 max-w-3xl mx-auto">
    <h1 class="text-2xl font-bold text-center mb-4">
      Selecciona las fechas que más te cuadren
    </h1>
    <CalendarView
      :show-date="showDate"
      :enable-date-selection="true"
      :starting-day-of-week="1"
      :selection-start="selectionStart"
      :selection-end="selectionEnd"
      :items="calendarEvents"
      class="theme-default holiday-us-traditional holiday-us-official border shadow-lg rounded-lg"
      @date-selection-finish="handleDateSelection"
      @click-date="handleClickDate"
    >
      <template #header="headerProps">
        <CalendarViewHeader v-bind="headerProps" @input="setShowDate" />
      </template>
    </CalendarView>
    <div class="flex justify-center gap-4 mt-4">
      <button
        @click="saveSelection"
        class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition"
      >
        Guardar Fechas
      </button>
      <button
        @click="clearSelection"
        class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition"
      >
        Borrar Fechas
      </button>
    </div>
    <div class="mt-4 flex justify-center gap-4">
      <input
        v-model="inputTitle"
        type="text"
        placeholder="Título del evento"
        class="px-4 py-2 border border-gray-300 rounded-lg"
      />
    </div>
    <div
      v-if="selectedDates.length"
      class="mt-6 p-4 bg-gray-100 rounded-lg shadow-md"
    >
      <h2 class="text-xl font-semibold">Has elegido:</h2>
      <ul class="mt-2 space-y-1">
        <li
          v-for="(date, index) in formattedDates"
          :key="index"
          class="text-blue-600 font-medium"
        >
          {{ date }}
        </li>
      </ul>
    </div>
    <p v-else class="text-center text-gray-500 mt-4">
      No hay fechas seleccionadas
    </p>
  </div>
</template>

<script>
import { CalendarView, CalendarViewHeader } from "vue-simple-calendar";
import axios from "axios";
import "../../node_modules/vue-simple-calendar/dist/vue-simple-calendar.css";
import "../../node_modules/vue-simple-calendar/dist/css/default.css";

export default {
  name: "app",
  data() {
    return {
      showDate: new Date(),
      selectionStart: null,
      selectionEnd: null,
      selectedDates: [],
      calendarEvents: [],
      inputTitle: "",
    };
  },
  async created() {
    this.selectedDates = await this.loadEventsFromServer(true);
    this.calendarEvents = await this.loadEventsFromServer(false);
  },
  components: { CalendarView, CalendarViewHeader },
  computed: {
    selectedEvents() {
      return [
        {
          id: "event-2025-03-03",
          startDate: "2025-03-03",
          endDate: "2025-03-05",
          title: "Futbol",
          tooltip: "Partido de Futbol",
          classes: ["selected-day"],
        },
        ...this.selectedDates.map((date) => ({
          id: `event-${date}`,
          startDate: date,
          endDate: date,
          title: this.inputTitle || "Fecha seleccionada",
          tooltip: "Evento seleccionado",
          classes: ["selected-day"],
        })),
      ];
    },
    formattedDates() {
      let currentRange = [];
      return this.selectedDates
        .sort((a, b) => new Date(a) - new Date(b))
        .reduce((formatted, date, index) => {
          const lastDate = new Date(currentRange[currentRange.length - 1] || 0);
          const currentDate = new Date(date);
          if (
            currentRange.length &&
            lastDate.getDate() + 1 === currentDate.getDate() &&
            lastDate.getMonth() === currentDate.getMonth() &&
            lastDate.getFullYear() === currentDate.getFullYear()
          ) {
            currentRange.push(date);
          } else {
            if (currentRange.length)
              formatted.push(this.formatRange(currentRange));
            currentRange = [date];
          }
          if (index === this.selectedDates.length - 1 && currentRange.length)
            formatted.push(this.formatRange(currentRange));
          return formatted;
        }, []);
    },
  },
  methods: {
    setShowDate(d) {
      this.showDate = d;
    },
    handleDateSelection([startDate, endDate]) {
      if (!startDate || !endDate || new Date(startDate) > new Date(endDate))
        return;

      this.selectionStart = startDate;
      this.selectionEnd = endDate;

      // Obtener las fechas en el rango
      const newDates = this.getDatesInRange(startDate, endDate);

      // Filtrar las nuevas fechas para que solo se agreguen las que no están ya en selectedDates
      this.selectedDates = [
        ...new Set([ // Mantener las fechas anteriores que no están en newDates
          ...newDates, // Añadir solo las nuevas fechas
        ]),
      ];
    },
    handleClickDate(date) {
      const formattedDate = this.formatDate(new Date(date));

      // Solo se agrega la fecha si no está ya en selectedDates
      if (!this.selectedDates.includes(formattedDate)) {
        this.selectedDates.push(formattedDate);
      }
    },
    getDatesInRange(startDate, endDate) {
      if (!startDate || !endDate || new Date(startDate) > new Date(endDate))
        return [];
      const dates = [];
      let currentDate = new Date(startDate);
      while (currentDate <= new Date(endDate)) {
        dates.push(this.formatDate(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
      }
      return dates;
    },

    // SECTION: SAVE SELECTION OF DATES

    async saveSelection() {
      console.log("selectedDates", this.selectedDates);
      const formattedDates = this.selectedDates.map((date) =>
        this.formatDate(new Date(date))
      );
      const eventTitle = this.inputTitle || "Evento sin título";
      const uuid = this.$route.params.uuid;
      if (!uuid) return alert("No se pudo encontrar el UUID en la URL.");
      const payload = {
        uuid,
        events: [{ title: eventTitle, dates: formattedDates }],
      };
      try {
        await axios.post("http://127.0.0.1:8000/save-dates/", payload, {
          headers: { "Content-Type": "application/json" },
        });
        localStorage.setItem("selectedDates", JSON.stringify(formattedDates));
        localStorage.setItem(
          "calendarEvents",
          JSON.stringify(this.calendarEvents)
        );
        alert("Fechas seleccionadas guardadas en el calendario!");
        this.selectedDates = [];
        this.inputTitle = "";
        window.location.reload();
      } catch (error) {
        console.error("Error al guardar las fechas:", error);
        alert("No se pudieron guardar las fechas.");
      }
    },

    // SECTION: CLEAR SELECTION OF DATES

    clearSelection() {
      this.selectedDates = [];
      this.calendarEvents = [];
      localStorage.removeItem("selectedDates");
      localStorage.removeItem("calendarEvents");
    },

    // SECTION: LOAD DATA FROM LOCAL STORAGE
    loadDatesFromLocalStorage() {
      console.log("localStorage dates", localStorage.getItem("selectedDates"));
      return JSON.parse(localStorage.getItem("selectedDates") || "[]");
    },
    loadEventsFromLocalStorage() {
      console.log(
        "localStorage events",
        localStorage.getItem("calendarEvents")
      );
      return JSON.parse(localStorage.getItem("calendarEvents") || "[]");
    },
    // SECTION: LOAD DATA FROM DB

    async loadEventsFromServer() {
      const uuid = this.$route.params.uuid;
      if (!uuid) {
        console.error("No se pudo encontrar el UUID en la URL.");
        return [];
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/retrieve-dates/${uuid}`
        );
        console.log("events", response.data.events);

        const transformedEvents = response.data.events.map((event) => {
          if (event.dates && event.dates.length > 0) {
            const startDate = event.dates[0];
            const endDate = event.dates[event.dates.length - 1];

            return {
              title: event.title,
              startDate,
              endDate,
            };
          } else {
            return {};
          }
        });
        console.log("transformedEvents", transformedEvents);
        return transformedEvents || [];
      } catch (error) {
        console.error("Error al cargar los eventos:", error);
        return [];
      }
    },

    // SECTION: FORMAT DATES
    formatRange(dates) {
      return dates.length === 1
        ? dates[0]
        : `del ${dates[0]} al ${dates[dates.length - 1]}`;
    },
    formatDate(date) {
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(
        2,
        "0"
      )}-${String(date.getDate()).padStart(2, "0")}`;
    },
  },
};
</script>
