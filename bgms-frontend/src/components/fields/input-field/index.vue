<template>
<div class="input-field w-full">
    <!-- input -->
    <input
        v-if="regularInput"
        ref="input"
        :class="{highlight: highlight}"
        :type="type"
        v-show="type!='multiselect'"
        :placeholder="placeholder"
        :value="modelValue"
        :disabled="disabled"
        :step="step"
        :min="min"
        :max="max"
        v-on:keypress="onInput($event)"
        @update:modelValue="modelValue = $event.target.value"
        @change="onChange"
        @keyup="onKeyup"
    />

    <!-- checkbox -->
    <input
        v-if="type === 'checkbox'"
        :type="type"
        :value="checkValue"
        :checked="modelValue === checkValue"
        :disabled="disabled"
        @update:modelValue="modelValue = $event.target.checked"
        @change="onChangeCheckbox"
    />

    <!-- radio input -->
    <fieldset class="flex w-full" v-if="type === 'radio'">
        <label
            class="radio-btn"
            v-for="option in options"
            :key="option.value"
        >
            <span>{{ option.label }}</span>
            <input
                :type="type"
                :name="radioId"
                :value="option.value"
                :checked="modelValue === option.value"
                :disabled="disabled"
                @update:modelValue="modelValue = $event.target.value"
                @change="onChange"
                @keyup="onKeyup"
            />
        </label>
    </fieldset>

    <!-- select -->
    <select
        :class="{default: modelValue === ''}"
        v-if="type === 'select'"
        :value="modelValue"
        :disabled="disabled"
        @update:modelValue="modelValue = $event.target.value"
        @change="onChange"
    >
        <option
            value=""
            hidden
            :selected="modelValue === ''"
        >
            {{ placeholder }}
        </option>
        <option
            v-for="option in options"
            :key="option.value"
            :value="option.value"
            :selected="modelValue === option.value"
        >
            {{ option.label }}
        </option>
    </select>

    <!-- multiselect -->
    <div class="multiselect-box" v-if="type === 'multiselect'">

    <select
        id="multiselect"
        :class="{default: modelValue === ''}"
        v-if="type === 'multiselect'"
        :value="modelValue"
        :disabled="disabled"
        @update:modelValue="modelValue = $event.target.value"
        @change="onChange"
    >
        <option
            v-for="option in options"
            :key="option.value"
            :value="option.value"
            :selected="modelValue === option.value"
        >
            {{ option.label }}
        </option>
        <option
            value=""
            hidden
            :selected="modelValue === ''"
        >
            {{ placeholder }}
        </option>
    </select>
    <div v-if="(getLabels(name)).length > 0" class="label-list">
        <span class="label-status" v-for="label in getLabels(name)">
          {{label}}
        </span>
    </div>
      <!--
      <span
            class="clear_x"
            v-if="type === 'multiselect'"
            @click="cleanValue"
        >
         <i class="icon-Clear-02-Filled" data-v-26a5cca2=""></i>
        </span>
        -->

    </div>
    <!-- textarea -->
    <textarea
        v-if="type === 'textarea'"
        :placeholder="placeholder"
        :value="modelValue"
        :disabled="disabled"
        @update:modelValue="modelValue = $event.target.value"
        @change="onChange"
        @keyup="onKeyup"
    >
    </textarea>

</div>
</template>

<style scoped src="./input-field.css"></style>

<script src="./input-field.js"></script>
