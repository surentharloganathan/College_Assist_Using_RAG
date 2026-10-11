package com.surenthar.rag.dto;


import jakarta.validation.constraints.NotBlank;
import lombok.Data;


@Data
public class QuestionRequest {

    @NotBlank(message = "question Should not be blank")
    private  String question;

}
