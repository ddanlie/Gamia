

<template>

    <div class="flex one textCenter">
        <h3 class="full">Start Writing!</h3>
        <h3 class="full">{{ minutesLeft }}:{{ secondsLeft.toString().padStart(2, '0') }}</h3>
        <textarea :disabled="timeLeft <= 0" v-model="this.prompt" class="full" style="resize: none;" rows=8 placeholder="New flavor of ice cream"></textarea>
    </div>

</template>


<script>

    export default {

        props: {
            secondsToWait : {
                type: Number,
                required: false
            },
        },

        watch : {
            prompt(prmpt)
            {
                this.$emit('promptReady', prmpt);
            }
        },

        mounted()
        {
            let tl = localStorage.getItem("timeLeft");
            if(tl)
            {
                this.timeLeft = tl-1 >= 0 ? tl-1 : tl;
            }
            else if(this.secondsToWait)
            {
                this.timeLeft = this.secondsToWait;
            }   
            this.counterInterval = setInterval(this.timeCounter, 1000);
        },

        unmounted()
        {
            localStorage.removeItem("timeLeft");
            clearInterval(this.counterInterval);
        },

        data() 
        {
            return {
                timeLeft: 0,
                prompt: "",
                mounted: false,
                counterInterval: null,
            }
        },

        methods: {

            timeCounter()
            {
                if(this.timeLeft <= 0)
                {
                    clearInterval(this.counterInterval);
                    localStorage.removeItem("timeLeft");
                    this.$emit('timeOut'); 
                    return;
                }

                this.timeLeft--;
                localStorage.setItem("timeLeft", this.timeLeft);
            }
        },

        computed: {

            minutesLeft() 
            {
                let tl = this.timeLeft;
                return Math.floor(tl / 60);
            },

            secondsLeft()
            { 
                let tl = this.timeLeft;
                return tl % 60; 
            }

        }, 

        
    }

</script>


<style scoped>

</style>