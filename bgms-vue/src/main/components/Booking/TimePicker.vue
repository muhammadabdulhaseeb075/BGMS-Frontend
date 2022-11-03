<template>
    <div>
        <v-text-field
         :ref="this.timeInputRef"
          v-model="timeValue"
          :label="this.timeInputLabel"
          :required="this.timeInputRequired"
          :rules="this.timeInputRules"
          @input="updateTimeParts"
          step="300"
          type=""
        >
          <template v-slot:append v-slot:activator="{ on }">
            <v-icon @click="showCardContainer = !showCardContainer">fas fa-clock</v-icon>
          </template>
        </v-text-field>
        <div class="time-container" v-if="showCardContainer">
          <v-card  class="v-card-time d-flex flex-row" width="200">
            <div ref="timeContainer" class="time-row">
              <div
                class="time-option"
                v-for="(hour) in hours"
                :key="'hour'+hour"
                v-bind:class="{ 'time-active': hourSelected === hour }"
                @click="selectHour(hour)"
              >{{ hour }}</div>
            </div>
            <div class="time-row">
              <div
                class="time-option"
                v-for="(minute) in minutes"
                :key="'minute'+minute"
                v-bind:class="{ 'time-active': minuteSelected === minute }"
                @click="selectMinutes(minute)"
              >{{ minute }}</div>
            </div>
            <div class="time-row">
              <div
                class="time-option"
                v-for="(meridiemCategory) in meridiemCategories"
                :key="'meridiemCategory'+meridiemCategory"
                v-bind:class="{ 'time-active': meridiemCategorySelected === meridiemCategory }"
                @click="selectMeridiemCategory(meridiemCategory)"
              >{{ meridiemCategory }}</div>
            </div>
          </v-card>
        </div>
    </div>
</template>

<script>
import moment from "moment";


const convertTimeToTwelveHourFormat = time => {
  return moment(time, "HH:mm").format("LT");
};

const convertTimeToTwentyFourHourFormat = time => {
  return moment(time, ["h:mm A"]).format("HH:mm");
};

const INITIAL_TIMEPICKER_PROPS = {
  hour: {
    default: "01"
  },
  minute: {
    default: "00"
  },
  meridiemCategory: {
    default: "p. m."
  },
  open: {
    default: false
  },
  value: {
    default: "13:00"
  },
  hours: {
    default: () => [
      "01",
      "02",
      "03",
      "04",
      "05",
      "06",
      "07",
      "08",
      "09",
      "10",
      "11",
      "12"
    ]
  },
  minutes: {
    default: () => [
      "00",
      "05",
      "10",
      "15",
      "20",
      "25",
      "30",
      "35",
      "40",
      "45",
      "50",
      "55"
    ]
  },
  timeInputLabel: {
    default: ""
  },
  timeInputRef: {
    default: undefined
  },
  timeInputRequired: {
    default: false
  },
  timeInputRules: {
    default: () => []
  }
};

export default {
  props: INITIAL_TIMEPICKER_PROPS,
   icons: {
    fontface: "md"
  },
  data: () => ({
    showCardContainer: INITIAL_TIMEPICKER_PROPS.open.default,
    hourSelected: INITIAL_TIMEPICKER_PROPS.hour.default,
    minuteSelected: INITIAL_TIMEPICKER_PROPS.minute.default,
    meridiemCategorySelected: INITIAL_TIMEPICKER_PROPS.meridiemCategory.default,
    meridiemCategories: ["p. m.", "a. m."]
  }),
  computed: {
    timeValue: {
      get() {
        return this.value ? this.value : INITIAL_TIMEPICKER_PROPS.value.default;
      },
      set(timeChanged) {
        this.$emit('input', timeChanged)
      }
    }
  },
  methods: {
    selectHour: function selectHour(hour) {
      this.hourSelected = hour;

      const formatMeridiemCategory =
        this.meridiemCategorySelected === "a. m." ? "AM" : "PM";

      const timeChanged = convertTimeToTwelveHourFormat(
        this.timeValue
      ).replace(/PM|AM/, formatMeridiemCategory);

      const timeFormatTwelveHours = timeChanged.replace(
        /^$|1|2|3|4|5|6|7|8|9|10|11|12/,
        this.hourSelected
      );

      this.timeValue = convertTimeToTwentyFourHourFormat(
        timeFormatTwelveHours
      );

    },
    selectMinutes: function selectMinutes(minute) {
      this.minuteSelected = minute;
      if (this.timeValue.length >= 5) {
        this.timeValue = this.timeValue.replace(/:\d\d/, ":" + minute);
      } else {
        this.timeValue = minute;
      }
    },
    selectMeridiemCategory: function selectMeridiemCategory(meridiemCategory) {
      this.meridiemCategorySelected = meridiemCategory;

      const formatMeridiemCategory = meridiemCategory === "a. m." ? "AM" : "PM";

      const timeChanged = convertTimeToTwelveHourFormat(
        this.timeValue
      ).replace(/PM|AM/, formatMeridiemCategory);

      this.timeValue = convertTimeToTwentyFourHourFormat(timeChanged);

    },
    updateTimeParts: function updateTimeParts(newTimeValue) {
      this.timeValue = newTimeValue;
      this.showCardContainer = false;
      const timeTwentyFourFormat = moment(newTimeValue, "HH:mm").format("LT");
      const partOfTime = timeTwentyFourFormat.split(":");
      const hour = partOfTime[0];

      if (hour.toString().length === 1) {
        this.hourSelected = `0${hour}`;
      } else {
        this.hourSelected = hour;
      }

      const minutesAndTMeridiemCategory = partOfTime[1].split(" ");
      const minute = minutesAndTMeridiemCategory[0];
      const meridiemCategory = minutesAndTMeridiemCategory[1];
      this.minuteSelected = minute;
      this.meridiemCategorySelected = meridiemCategory === "AM" ? "a. m." : "p. m.";
    }
  }
};
</script>

<style>
input[type="time"]::-webkit-calendar-picker-indicator {
  display: none;
}

.time-container {
    position: fixed;
    margin-top: -15px;
    width: 180px;
    z-index: 100;
}

.time-row {
    flex: 1;
    align-content: center;
    justify-content: center;
    margin: 2px;
    height: 220px;
    overflow: scroll;
}

div.time-row::-webkit-scrollbar {
  display: none;
}

.time-option {
    border: solid transparent 2px;
    text-align: center;
    padding: 6px;
}
.time-option:hover {
     cursor: pointer;
        background-color: rgba( 206, 206 , 206, 0.4);
}

.time-active {
    background-color: rgb( 206, 206 , 206);
    font-weight: bold;
    border: solid 2px;
}
</style>
