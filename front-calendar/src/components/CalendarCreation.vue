<template>
    <div id="app" class="p-6 max-w-3xl mx-auto">
        <h1 class="text-2xl font-bold text-center mb-4">Selecciona las fechas que más te cuadren</h1>

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
            <button @click="saveSelection" class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition">
                Guardar Fechas
            </button>
            <button @click="clearSelection"
                class="px-4 py-2 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition">
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

        <div v-if="selectedDates.length" class="mt-6 p-4 bg-gray-100 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold">Has elegido:</h2>
            <ul class="mt-2 space-y-1">
                <li v-for="(date, index) in formattedDates" :key="index" class="text-blue-600 font-medium">
                    {{ date }}
                </li>
            </ul>
        </div>
        <p v-else class="text-center text-gray-500 mt-4">No hay fechas seleccionadas</p>
    </div>
</template>

<script>
import { CalendarView, CalendarViewHeader } from "vue-simple-calendar";
import "../../node_modules/vue-simple-calendar/dist/vue-simple-calendar.css";
import "../../node_modules/vue-simple-calendar/dist/css/default.css";

export default {
    name: "app",
    data() {
        return {
            showDate: new Date(),
            selectionStart: null,
            selectionEnd: null,
            selectedDates: this.loadDatesFromLocalStorage(), // Cargar fechas guardadas en localStorage
            calendarEvents: this.loadEventsFromLocalStorage(), // Cargar eventos desde localStorage
            inputTitle: "" // El valor del input para el título
        };
    },
    components: {
        CalendarView,
        CalendarViewHeader,
    },
    computed: {
        selectedEvents() {
            // Aquí combinamos el evento de fútbol con los eventos seleccionados
            return [
                {
                    id: "event-2025-03-03", 
                    startDate: "2025-03-03",
                    endDate: "2025-03-05",
                    title: "Futbol", 
                    tooltip: 'Partido de Futbol',
                    classes: ['selected-day'], 
                },
                // Mapeamos las fechas seleccionadas como eventos
                ...this.selectedDates.map(date => ({
                    id: `event-${date}`, // ID único para cada evento basado en la fecha
                    startDate: date,
                    endDate: date,
                    title: this.inputTitle || "Fecha seleccionada", // Usamos el valor del input como título
                    tooltip: 'Evento seleccionado', 
                    classes: ['selected-day'], 
                }))
            ];
        },
        formattedDates() {
            const formatted = [];
            let currentRange = [];
            
            this.selectedDates.sort((a, b) => new Date(a) - new Date(b)).forEach((date, index) => {
                if (currentRange.length === 0) {
                    currentRange.push(date);
                } else {
                    const lastDate = new Date(currentRange[currentRange.length - 1]);
                    const currentDate = new Date(date);

                    if (lastDate.getDate() + 1 === currentDate.getDate() &&
                        lastDate.getMonth() === currentDate.getMonth() &&
                        lastDate.getFullYear() === currentDate.getFullYear()) {
                        currentRange.push(date); 
                    } else {
                        formatted.push(this.formatRange(currentRange));
                        currentRange = [date];
                    }
                }
            });

            if (currentRange.length > 0) {
                formatted.push(this.formatRange(currentRange));
            }

            return formatted;
        },
    },
    methods: {
        setShowDate(d) {
            this.showDate = d;
        },
        handleDateSelection([startDate, endDate]) {
            if (!startDate || !endDate || new Date(startDate) > new Date(endDate)) return;
            this.selectionStart = startDate;
            this.selectionEnd = endDate;
            const newDates = this.getDatesInRange(startDate, endDate);
            this.selectedDates = [...new Set([...this.selectedDates, ...newDates])];
        },
        handleClickDate(date) {
            const formattedDate = this.formatDate(new Date(date)); // Usamos el nuevo método formatDate
            if (!this.selectedDates.includes(formattedDate)) {
                this.selectedDates.push(formattedDate); 
            }
        },
        getDatesInRange(startDate, endDate) {
            if (!startDate || !endDate || new Date(startDate) > new Date(endDate)) return [];
            const dates = [];
            let currentDate = new Date(startDate);
            while (currentDate <= new Date(endDate)) {
                dates.push(this.formatDate(currentDate)); // Formateamos las fechas aquí también
                currentDate.setDate(currentDate.getDate() + 1);
            }
            return dates;
        },
        saveSelection() {
            const newEvents = this.selectedEvents; // Crear nuevos eventos con las fechas seleccionadas
            this.calendarEvents = [...this.calendarEvents, ...newEvents];
            
            // Guardar las fechas en formato yyyy-mm-dd
            const formattedDates = this.selectedDates.map(date => this.formatDate(new Date(date)));
            console.log(this.calendarEvents)
            localStorage.setItem("selectedDates", JSON.stringify(formattedDates)); // Guardar en localStorage
            localStorage.setItem("calendarEvents", JSON.stringify(this.calendarEvents)); // Guardar eventos en localStorage
            alert("Fechas seleccionadas guardadas en el calendario!");
            this.selectedDates = []; // Limpiar la selección después de guardarla
            this.inputTitle = ""; // Limpiar el input de título después de guardar
        },
        clearSelection() {
            this.selectedDates = [];
            this.calendarEvents = [];
            localStorage.removeItem("selectedDates");
            localStorage.removeItem("calendarEvents");
        },
        loadDatesFromLocalStorage() {
            const savedDates = localStorage.getItem("selectedDates");
            return savedDates ? JSON.parse(savedDates) : [];
        },
        loadEventsFromLocalStorage() {
            const savedEvents = localStorage.getItem("calendarEvents");
            return savedEvents ? JSON.parse(savedEvents) : [];
        },
        formatRange(dates) {
            if (dates.length === 1) {
                return dates[0]; 
            } else {
                return `del ${dates[0]} al ${dates[dates.length - 1]}`;
            }
        },
        formatDate(date) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0'); // Asegurarse de que el mes tenga 2 dígitos
            const day = String(date.getDate()).padStart(2, '0'); // Asegurarse de que el día tenga 2 dígitos
            return `${year}-${month}-${day}`;
        }
    },
};
</script>

