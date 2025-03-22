<template>
  <div
    class="min-h-screen flex flex-col items-center sm:items-center justify-center bg-gradient-to-br from-purple-600 to-blue-500 text-white px-6 text-center">
    <!-- Ajusta el valor de ml-4 según sea necesario -->
    <h1 class="text-7xl sm:text-9xl font-extrabold tracking-wide drop-shadow-lg animate-fade-in">
      PikaDate
    </h1>
    <p class="text-lg sm:text-xl mt-4 opacity-90 max-w-lg animate-fade-in delay-200">
      Elige las mejores fechas para tus viajes, eventos o reuniones.
    </p>
    <button
  class="mt-8 bg-white text-gray-800 font-semibold py-2 px-4 rounded-lg shadow-lg animate-fade-in delay-400 cursor-pointer hover:bg-gray-200 transition-none"
  @click="handleClick"
>
  ¡Crea tu calendario!
</button>

  
  </div>
    <button
      class="flex flex-col items-end justify-end fixed bottom-4 right-4 animate-fade-in delay-400 hover:cursor-pointer"
      @click="handleClickGithub"
    >
        <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        aria-hidden="true"
        focusable="false"
        >
            <path
            d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"
            fill="white"
            />
      </svg>
    </button>
    <button
      class="flex flex-col items-end justify-end fixed bottom-4 right-4 animate-fade-in delay-400 mr-10 hover:cursor-pointer"
      @click="handleClickLinkedin"
    >
        <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        aria-hidden="true"
        focusable="false"
        >
            <path
            d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"
            fill="white"
            />
        </svg>
    </button>

</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const handleClickGithub = () => {
  window.open("https://github.com/jaimemartinez-99/", "_blank");
}

const handleClickLinkedin = () => {
  window.open("https://www.linkedin.com/in/jaime-martínez-ramón-4588522a6", "_blank");
}

const handleClick = () => {
  router.push("/calendarCreation");
}

</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}
</style>
