


<template>

        <button @click="this.$emit('readyPressed')" class="two-third" :class="!ready ? 'greenBack':  'redBack'">
            <h2 class="zeroPad blackColor">
                {{!ready ? "Ready" : "Cancel"}}
            </h2>
        </button>

</template>


<script>
    export default {
        props: ['ready'],
        data()
        {
            return {
            }
        },

        methods: {
        }
    }
</script>